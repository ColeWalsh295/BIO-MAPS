# Module UI functions
# corresponding server functions use the same function name with 'UI' removed from the end

library(shiny)
library(shinyBS)

DownloadClassDataUI <- function(id, label, value){
  # create textbox for class ID input and download button for class data
  
  # Create a namespace function using the provided id
  ns <- NS(id)
  
  fluidRow(
    column(4, textInput(ns('classID'), label, value)),
    column(3, br(), downloadButton(ns("downloadData"), "Download", class = 'button') %>%
             helper(icon = "question",
                    colour = "green",
                    type = "markdown",
                    content = "downloads"))
  )
}

ClassStatisticsOutput <- function(id, Overall = FALSE){
  # create summary statistics boxes
  
  ns <- NS(id)
  
  if(Overall){
    fluidRow(
      radioButtons(ns("class.level"), 'Compare to other classes:',
                   choiceNames = c('All', 'Beginning of intro course series', 
                                   'End of intro course series', 
                                   'Advanced',
                                   'Graduate'),
                   choiceValues = c('All', 'Begin_Intro', 'End_Intro', 'Advanced', 'Graduate'), inline = TRUE),
      valueBoxOutput(ns("infoNStudents")),
      infoBoxOutput(ns("infoScore"))
    )
  } else {
    fluidRow(
      valueBoxOutput(ns("infoNStudents")),
      infoBoxOutput(ns("infoScore"))
    )
  }
}

ScalePlotUI <- function(id, Demos = TRUE, MatchBox = FALSE){
  # create boxplots of students' scores on selected dimensions
  
  ns <- NS(id)
  
  if(Demos) {
    fluidPage(
      fluidRow(
        column(4, selectInput(ns("scale"), "Question Categorization:", 
                              choices = c('Subdisciplines', 'Core concepts'))),
        column(4, radioButtons(ns("demographic"), 'Separate by:',
                               choiceNames = c('None', 'Gender', 'URM Status', 
                                               'First Generation Status', 'Class Standing', 
                                               'Major', 'Transfer Status', 
                                               'Primary Language spoken at Home'),
                               choiceValues = c('None', 'SexGender', 'URMStatus', 
                                                'ParentEducation', 'ClassStanding', 
                                                'Major', 'TransferStatus', 'ELL')) %>%
                 helper(icon = "question",
                        colour = "blue",
                        type = "markdown",
                        content = "demographics")),
        plotOutput(ns("plotScale"))
      )
    )
  } else if(MatchBox){
    fluidRow(
      column(4, selectInput(ns("scale"), "Question Categorization:", 
                            choices = c('Subdisciplines', 'Core concepts'))),
      column(4, checkboxInput(ns("match"), "Match Class Data", value = FALSE)),
      br(),
      plotOutput(ns("plotScale"))
    )
  } else {
    fluidRow(
      column(4, selectInput(ns("scale"), "Question Categorization:", 
                            choices = c('Subdisciplines', 'Core concepts'))),
      br(),
      plotOutput(ns("plotScale"))
    )
  }
}

ResponsesPlotUI <- function(id, Demos = TRUE){
  # create bar plots of fraction of students getting items correct on selected questions
  
  ns <- NS(id)
  
  fluidRow(
    column(2, selectInput(ns("question"), "Question:", 
                          choices = c('01', '02', '03', '04', '07', '08', '12', '13', '14',
                                      '15', '16', '18', '19', '20', '21', '22', '23', '24', 
                                      '27', '28', '30', '31', '32', '33', '35', '36', '37', 
                                      '38', '40', '43', '44', '45', '49', '50', '54', '55', 
                                      '59', '60', '61'))),
    column(10, plotOutput(ns("plotResponses")))
  )
}

radioTooltip <- function(id, choice, title, placement = "right", trigger = "hover", 
                         options = NULL){
  # adds the little text that appears when you hover over the radio button
  options = shinyBS:::buildTooltipOrPopoverOptionsList(title, placement, trigger, options)
  options = paste0("{'", paste(names(options), options, sep = "': '", collapse = "', '"), 
                   "'}")
  bsTag <- shiny::tags$script(shiny::HTML(paste0("
                                                 $(document).ready(function() {
                                                 setTimeout(function() {
                                                 $('input', $('#", id, "')).each(function(){
                                                 if(this.getAttribute('value') == '", choice, "') {
                                                 opts = $.extend(", options, ", {html: true});
                                                 $(this.parentElement).tooltip('destroy');
                                                 $(this.parentElement).tooltip(opts);
                                                 }
                                                 })
                                                 }, 500)
                                                 });
                                                 ")))
  htmltools::attachDependencies(bsTag, shinyBS:::shinyBSDep)
}