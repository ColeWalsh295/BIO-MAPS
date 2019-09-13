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

ScalePlotUI <- function(id, Demos = TRUE, MatchBox = FALSE){
  ns <- NS(id)
  
  if(Demos) {
    fluidRow(
      column(4, selectInput(ns("scale"), "Scale:", 
                            choices = c('Overall Scores', 'Vision and Change'))),
      column(8, radioButtons(ns("demographic"), 'Separate by:',
                             choiceNames = c('None', 'Gender', 'URM Status', 'First Generation Status', 
                                              'Class Standing', 'Major', 'Transfer Status', 
                                              'English Language Learners'),
                             choiceValues = c('None', 'Self-Declared_Sex/Gender', 'URM_Status', 'First_Generation_Status', 'Class_Standing', 'Intended_Major', 'Transfer_Status', 
                                              'English_Language_Learner_Status'))),
      plotOutput(ns("plotScale"))
    )
  } else if(MatchBox){
    fluidRow(
      column(4, selectInput(ns("scale"), "Scale:", 
                            choices = c('Overall Scores', 'Vision and Change'))),
      column(4, checkboxInput(ns("match"), "Match Class Data", value = FALSE)),
      br(),
      plotOutput(ns("plotScale"))
    )
  } else {
    fluidRow(
      column(4, selectInput(ns("scale"), "Scale:", 
                            choices = c('Overall Scores', 'Vision and Change'))),
      br(),
      plotOutput(ns("plotScale"))
    )
  }
}

ResponsesPlotUI <- function(id, Demos = TRUE){
  ns <- NS(id)
  
  fluidRow(
    column(2, selectInput(ns("question"), "Question:", 
                          choices = c('01', '02', '03', '04', '07', '08', '12', '13', '14', '15', 
                                      '16', '18', '19', '20', '21', '22', '23', '24', '27', '28',
                                      '30', '31', '32', '33', '35', '36', '37', '38', '40', '43',
                                      '44', '45', '49', '50', '54', '55', '59', '60', '61'))),
    column(10, plotOutput(ns("plotResponses")))
  )
}