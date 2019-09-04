DownloadClassDataUI <- function(id, label, value){
  # Create a namespace function using the provided id
  ns <- NS(id)
  
  fluidRow(
    column(4, textInput(ns('classID'), label, value)),
    column(4, br(), downloadButton(ns("downloadData"), "Download", class = 'button'))
  )
}

ClassStatisticsOutput <- function(id){
  ns <- NS(id)
  
  fluidRow(
    valueBoxOutput(ns("infoNStudents")),
    infoBoxOutput(ns("infoScore"))
  )
}

ScalePlotUI <- function(id, Demos = TRUE){
  ns <- NS(id)
  
  if(Demos) {
    fluidRow(
      column(4, selectInput(ns("scale"), "Scale:", 
                            choices = c('Overall Scores', 'Vision and Change',
                                        'Ecology and Evolution Core Concepts', '4DEE Framework'))),
      column(8, radioButtons(ns("demographic"), 'Separate by:',
                             choices = c('None', 'Gender', 'URM Status', 'Major', 'Class Standing',
                                         'First Generation Status'), inline = TRUE)),
      br(),
      plotOutput(ns("plotScale"))
    )
  } else {
    fluidRow(
      column(4, selectInput(ns("scale"), "Scale:", 
                            choices = c('Overall Scores', 'Vision and Change',
                                        'Ecology and Evolution Core Concepts', '4DEE Framework'))),
      br(),
      plotOutput(ns("plotScale"))
    )
  }
}

ResponsesPlotUI <- function(id, Demos = TRUE){
  ns <- NS(id)
  
  fluidRow(
    column(2, selectInput(ns("question"), "Question:", 
                          choices = c('Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9'))),
    column(10, plotOutput(ns("plotResponses")))
  )
}