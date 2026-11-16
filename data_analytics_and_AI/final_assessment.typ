#set document(title: "Data analytics and AI — final assessment")
#set page(paper: "a4", margin: (x: 18mm, y: 16mm))
#set text(font: "Arial", size: 10pt, lang: "en")
#set par(leading: 0.5em, justify: false)

#let ink = rgb("202020")
#let muted = rgb("696969")
#let rule = rgb("cdcdcd")

#let question(n, prompt, choices) = [
  #block(breakable: false)[
    #grid(
      columns: (10mm, 1fr),
      gutter: 2mm,
      [#text(weight: "bold", fill: muted)[#n]],
      [#text(weight: "medium")[#prompt]
        #v(1.5mm)
        #grid(
          columns: (1fr, 1fr), column-gutter: 5mm, row-gutter: 3mm,
          ..choices.map(choice => [#stack(
            dir: ltr,
            spacing: 2mm,
            rect(width: 3mm, height: 3mm),
            choice,
          )])
        )
      ],
    )
  ]
  #v(4mm)
  #v(4mm)
]

#let open-page(n, prompt) = [
  #align(right)[#text(size: 9pt, fill: muted)[OPEN RESPONSE  #n]]
  #v(2mm)
  #text(weight: "bold", size: 11pt)[#prompt]
  #v(6mm)
  #for _ in range(19) {
    line(length: 100%, stroke: 0.5pt + rule)
    v(8.5mm)
  }
]

#text(
  size: 9pt,
  weight: "bold",
  tracking: 1pt,
  fill: muted,
)[DATA ANALYTICS AND AI]
#v(0mm)
#text(size: 22pt, weight: "bold")[Final assessment]
#v(2mm)
#text(size: 11pt, fill: muted)[60 minutes (30-minute quiz · 30-minute open questions)]
#v(8mm)
#grid(
  columns: (1fr, 1fr),
  column-gutter: 10mm,
  [Name: #line(length: 65mm, stroke: 0.5pt + rule)],
  [Date: #line(length: 45mm, stroke: 0.5pt + rule)],
)
#v(6mm)
#line(length: 100%, stroke: 0.7pt + ink)
#v(5mm)
#text(weight: "bold")[Instructions]
#v(1mm)
#text(size: 9.5pt)[
  Complete the 15 multiple-choice questions. Select one answer for each question by marking its box.
]
#v(6mm)
#text(size: 11pt, weight: "bold")[Quiz · 30 minutes]
#v(3mm)

#question("01", [Which description best fits *smart data*?], (
  [The largest dataset a company can collect],
  [Data prepared and contextualised for a specific decision],
  [Data generated only by artificial intelligence],
  [Any dataset made publicly available],
))
#question(
  "02",
  [A company wants to estimate next month's customer spending. What kind of task is this?],
  (
    [Classification],
    [Regression],
    [Sentiment analysis],
    [Clustering],
  ),
)
#question("03", [In a churn prediction project, which is the target?], (
  [Customer age],
  [Monthly fee],
  [Whether the customer churns],
  [Number of support calls],
))
#question(
  "04",
  [Why keep a test set separate when training a predictive model?],
  (
    [To evaluate performance on examples not used for fitting],
    [To remove every missing value],
    [To make the training data larger],
    [To choose the business question after fitting],
  ),
)
#question(
  "05",
  [A model performs very well on training examples but poorly on new examples. This is most likely…],
  (
    [underfitting],
    [overfitting],
    [data aggregation],
    [random sampling],
  ),
)

#pagebreak()

#text(
  size: 9pt,
  weight: "bold",
  tracking: 1pt,
  fill: muted,
)[DATA ANALYTICS AND AI  /  QUIZ]
#v(5mm)
#text(size: 16pt, weight: "bold")[Choose one answer for each question]
#v(7mm)
#question(
  "06",
  [A dataset has many more non-churners than churners. Which statement about accuracy is most useful?],
  (
    [High accuracy always means churners are identified well],
    [A model predicting no churn for everyone may still have high accuracy],
    [Accuracy measures only the number of features],
    [Accuracy is unaffected by class balance],
  ),
)
#question(
  "07",
  [A retention campaign is inexpensive, and missing a likely-to-churn customer is costly. Which metric should receive particular attention?],
  (
    [Recall],
    [Precision only],
    [R²],
    [Mean absolute error],
  ),
)
#question(
  "08",
  [What usually happens when the probability threshold for a purchase campaign is raised?],
  (
    [More customers are selected, including less certain cases],
    [Fewer customers are selected, generally with higher predicted likelihood],
    [The model is retrained on the test set],
    [The target changes from a category to a number],
  ),
)

#question(
  "09",
  [Why can feature scaling matter for a K-nearest neighbors model?],
  (
    [Features with larger numeric ranges can dominate distance],
    [It converts categories into review text],
    [It guarantees perfect test performance],
    [It removes the need for a target variable],
  ),
)
#question(
  "10",
  [A product review says, “Great, another broken bottle.” Why might a simple positive/negative word counter fail?],
  (
    [It cannot read any text],
    [It may miss context such as sarcasm],
    [It automatically knows the customer's intention],
    [It requires a numeric target],
  ),
)

#pagebreak()

#text(
  size: 9pt,
  weight: "bold",
  tracking: 1pt,
  fill: muted,
)[DATA ANALYTICS AND AI  /  QUIZ]
#v(5mm)
#text(size: 16pt, weight: "bold")[Choose one answer for each question]
#v(7mm)
#question("11", [What does a basic bag-of-words representation usually lose?], (
  [The count of each word],
  [The order of words],
  [The number of reviews],
  [The sentiment labels],
))
#question(
  "12",
  [When evaluating a text classifier, why should the vocabulary be learned from training reviews only?],
  (
    [To keep test information out of model fitting],
    [To make every review the same length],
    [To ensure unknown words become positive],
    [To avoid assigning labels to training data],
  ),
)
#question("13", [Which choice is an example of structured data?], (
  [A table of orders with date, price, and product columns],
  [A folder of customer voice recordings],
  [A collection of product photographs],
  [A set of free-form email messages],
))
#question(
  "14",
  [A customer field is missing because some customers chose not to disclose it. What should an analyst do first?],
  (
    [Replace every missing value with zero],
    [Consider why it is missing and how that affects the analysis],
    [Delete the entire dataset],
    [Assume the missingness is completely random],
  ),
)
#question(
  "15",
  [A team plans to use sensitive customer data for personalised offers. What is the best next step?],
  (
    [Use all available data because it may improve accuracy],
    [Check privacy, consent, potential bias, and explain the use],
    [Hide the model's decisions from customers],
    [Share the data openly so the model can be checked],
  ),
)

#pagebreak()
#open-page(
  "A",
  [A subscription company wants to reduce customer churn. Describe a sound data and modelling approach: state a useful target and possible features, explain how you would prepare the data and evaluate the model, and name one ethical or practical risk to manage.],
)

#pagebreak()
#open-page(
  "B",
  [A retailer has customer reviews and campaign results. Propose one useful analysis that could guide a marketing decision. Explain what data you would use, how you would analyse or present it, what action the business could take, and one limitation or ethical concern.],
)
