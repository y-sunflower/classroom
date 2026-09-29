class CsvTable extends HTMLElement {
  connectedCallback() {
    if (this.dataset.loaded) return;
    this.dataset.loaded = "true";
    this.loadTable();
  }

  async loadTable() {
    const source = this.getAttribute("src");
    const caption = this.getAttribute("caption") || "CSV data";
    const pageSize = Number.parseInt(
      this.getAttribute("page-size") || "15",
      15,
    );
    const search = document.createElement("input");
    search.type = "search";
    search.placeholder = "Search";
    search.setAttribute("aria-label", `Search ${caption}`);

    const tableElement = document.createElement("div");
    tableElement.setAttribute("aria-label", caption);
    const status = document.createElement("p");
    status.className = "csv-table__status";
    status.setAttribute("role", "status");
    status.textContent = "Loading table…";
    this.replaceChildren(search, status, tableElement);

    try {
      if (!source)
        throw new Error("Add a src attribute with the path to a CSV file.");
      const response = await fetch(source);
      if (!response.ok)
        throw new Error(`Could not load the CSV (${response.status}).`);

      const table = new Tabulator(tableElement, {
        data: await response.text(),
        importFormat: "csv",
        autoColumns: true,
        layout: "fitDataStretch",
        pagination: true,
        paginationSize: pageSize > 0 ? pageSize : 10,
        paginationSizeSelector: true,
      });

      search.addEventListener("input", () => {
        const query = search.value.trim().toLocaleLowerCase();
        table.setFilter((row) =>
          Object.values(row).some((value) =>
            String(value).toLocaleLowerCase().includes(query),
          ),
        );
      });
      status.remove();
    } catch (error) {
      status.className = "csv-table__status csv-table__error";
      status.setAttribute("role", "alert");
      status.textContent =
        error instanceof Error
          ? error.message
          : "Could not load this CSV file.";
    }
  }
}

if (!customElements.get("csv-table"))
  customElements.define("csv-table", CsvTable);
