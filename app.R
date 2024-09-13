library(shiny)
library(tidyverse)
library(rsconnect)

data_into_long <- function(x) {
    # Remove square brackets
    cleaned <- str_remove_all(x, "^\\[|\\]$")
    # Split by "), (" to separate each pair
    pairs <- str_split(cleaned, "\\), \\(")[[1]]
    # Parse each pair
    result <- map(pairs, function(pair) {
      # Extract faculty and discipline
      match <- str_match(pair, "'(.+)', '(.+)'")
      tibble(faculty = match[1,2], discipline = match[1,3])
      })
    bind_rows(result)
}

# Data
data_long <- read_csv("sentiment_analysis.csv") %>%
  mutate(each_df = map(discipline_faculty, data_into_long)) %>%
  unnest(each_df) %>%
  select(-3)

# UI
ui <- fluidPage(
  titlePanel("Sentimental Comparison of University of Auckland Related Reddit Posts"),
  sidebarLayout(
    sidebarPanel(
      selectInput("selection_type", "Select Type:", choices = c("Discipline" = "discipline", "Faculty" = "faculty")),
      selectizeInput("specific_choices", "Choose Disciplines or Faculties:", choices = NULL, multiple = TRUE)
    ),
    mainPanel(
      plotOutput("sentimentPlot")
    )
  )
)


# Server
server <- function(input, output, session) {
  observe({
    updateSelectizeInput(session, "specific_choices",
                         choices = unique(data_long[[input$selection_type]]),
                         server = TRUE)
  })
  
  output$sentimentPlot <- renderPlot({

    filtered_data <- data_long %>%
      filter(.[[input$selection_type]] %in% input$specific_choices)
    
    ggplot(filtered_data, aes_string(x = input$selection_type, y = "sentiment_score", fill = input$selection_type)) +
      geom_boxplot() +
      labs(title = paste("Boxplot of Sentiment Scores for Selected", input$selection_type),
           x = input$selection_type, y = "Sentiment Score") +
      theme_minimal() +
      theme(axis.text.x = element_text(angle = 45, hjust = 1))
  })
}

shinyApp(ui = ui, server = server)


