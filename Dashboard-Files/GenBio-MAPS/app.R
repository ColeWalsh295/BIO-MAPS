library(tidyverse)
library(shiny)
library(shinyjs)
library(shinyalert)
shiny_theme <- theme_classic(base_size = 18)
library(shinydashboard)
library(data.table)
library(reshape2)
library(rsconnect)
#source('PLIC_DataProcessing.R', local = TRUE)
source('GenBio_UI.R', local = TRUE)
source('GenBio_Server.R', local = TRUE)

# Get Complete dataset
df <- fread('C:/Users/Cole/Documents/GRA_Fall2019/BIO-MAPS_Shiny/GenBio-MAPS/GenBio-MAPS_MasterFile.csv')
df <- data.table(df)[, N.Students := .N, by = .(Course)]

Your_tab = tabItem(
  tabName = "Your_Class",
  h2("View of your class"),
  
  DownloadClassDataUI('Class.Main.Download', label = 'Your Class ID:', value = 'R_0vU5WDrHWLjYc37'),
  br(),
  ClassStatisticsOutput('Class.Main.Statistics'),
  br(),
  ScalePlotUI('Class.Main.Scale', Demos = TRUE),
  br(),br(),br(),br(),br(),
  ResponsesPlotUI('Class.Main.Responses', Demos = TRUE)
)

Compare_tab = tabItem(
  tabName = "Compare_Classes",
  h2("Compare two of your classes"),
  
  DownloadClassDataUI('Class1.Download', label = 'Your first Class ID:',
                      value = 'R_0vU5WDrHWLjYc37'),
  br(),
  ClassStatisticsOutput('Class1.Statistics'),
  DownloadClassDataUI('Class2.Download', label = 'Your second Class ID:',
                      value = 'R_3m4zpoFjt1eXUAI'),
  br(),
  ClassStatisticsOutput('Class2.Statistics'),
  ScalePlotUI('Class.Compare.Scale', Demos = FALSE),
  br(), br(), br(), br(), br(),
  ResponsesPlotUI('Class.Compare.Responses', Demos = FALSE)
)

Overall_tab = tabItem(
  tabName = "Compare_Overall",
  h2("Compare your classes to other classes"),
  
  DownloadClassDataUI('Class.You.Download', label = 'Your Class ID:',
                      value = 'R_0vU5WDrHWLjYc37'),
  br(),
  ClassStatisticsOutput('Class.You.Statistics'),
  br(),
  h3("Other classes"),
  ClassStatisticsOutput('Class.Other.Statistics'),
  br(),
  ScalePlotUI('Overall.Compare.Scale', Demos = FALSE),
  br(), br(), br(), br(), br(),
  ResponsesPlotUI('Overall.Compare.Responses', Demos = FALSE)
)

server = function(input, output) {
  
  ### Your Class ###
  
  df.Class <- callModule(DownloadClassData, 'Class.Main.Download', data = df)
  callModule(ClassStatistics, 'Class.Main.Statistics', data = df.Class)
  demographic <- reactiveVal()
  demographic <- callModule(ScalePlot, 'Class.Main.Scale', data = df.Class)
  callModule(ResponsesPlot, 'Class.Main.Responses', data = df.Class, Demo = demographic)
  
  ### Compare Classes ###
  
  df.Class1 <- callModule(DownloadClassData, 'Class1.Download', data = df)
  callModule(ClassStatistics, 'Class1.Statistics', data = df.Class1)
  df.Class2 <- callModule(DownloadClassData, 'Class2.Download', data = df)
  callModule(ClassStatistics, 'Class2.Statistics', data = df.Class2)
  
  df.Compare <- reactive({
    rbind(df.Class1(), df.Class2())
  })
  callModule(ScalePlot, 'Class.Compare.Scale', data = df.Compare, Class.var = 'Class_ID')
  callModule(ResponsesPlot, 'Class.Compare.Responses', data = df.Compare, Class.var = 'Class_ID')
  
  ### Compare to overall PLIC dataset ###
  
  df.Class.You_temp <- callModule(DownloadClassData, 'Class.You.Download', data = df)
  callModule(ClassStatistics, 'Class.You.Statistics', data = df.Class.You_temp)
  
  df.Class.You <- reactive({
    df.Class.You <- df.Class.You_temp() %>%
      mutate(Class = 'Your Class')
    return(df.Class.You)
  })
  df.Class.Other <- reactive({
    df.Class.Other <- df[df$Class_ID != df.Class.You_temp()$Class_ID[1],] %>%
      mutate(Class = 'Other Classes')
    return(df.Class.Other)
  })
  callModule(ClassStatistics, 'Class.Other.Statistics', data = df.Class.Other, Overall = TRUE)
  
  df.Overall <- reactive({
    rbind(df.Class.You(), df.Class.Other())
  })
  callModule(ScalePlot, 'Overall.Compare.Scale', data = df.Overall, Class.var = 'Class')
  callModule(ResponsesPlot, 'Overall.Compare.Responses', data = df.Overall, Class.var = 'Class')
}

# Set up the Header of the dashboard
dhead = dashboardHeader(title = h1(HTML("EcoEvo-MAPS<br>Data Explorer")))

# Set up the sidebar which links to two pages
dside = dashboardSidebar(sidebarMenu(
  id = 'tabs',
  menuItem("View of your class", tabName = "Your_Class", icon = icon("dashboard")),
  menuItem(HTML("Compare two of<br>your classes"), tabName = "Compare_Classes", icon = icon("dashboard")),
  menuItem(HTML("Compare your class<br>to other classes"), tabName = "Compare_Overall", 
           icon = icon("dashboard"))
))

# Here we set up the body of the dashboard
dbody = dashboardBody(
 tags$head(
   tags$link(rel = "stylesheet", type = "text/css",
             href = "Cornell.css")
 ),
  tabItems(Your_tab, Compare_tab, Overall_tab)
)

# Combining header, sidebar, and body
ui = dashboardPage(dhead, dside, dbody)

# Generating a local instance of your dashboard
shinyApp(ui, server)