// Add an onload event handler to the Qualtrics survey engine
Qualtrics.SurveyEngine.addOnload(function() {
    // Define an array of question IDs for two blocks (Q1 and Q2)
    let blockQuestions = [
        "Q1_1A", "Q1_2", "Q1_3", "Q1_4", "Q1_5", "Q1_6", "Q1_7", "Q1_8", "Q1_9", "Q1_10", "Q1_11", "Q1_12",
        "Q2_1A", "Q2_2", "Q2_3", "Q2_4", "Q2_5", "Q2_6", "Q2_7", "Q2_8", "Q2_9", "Q2_10", "Q2_11", "Q2_12"
    ];

    // Create an array of available question indices (1 to 12)
    let availableQuestions = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12];

    // Initialize an empty array to store selected questions
    let selectedQuestions = [];

    // Randomly select 3 questions from the first block (Q1)
    while (selectedQuestions.length < 3) {
        // Generate a random index from the availableQuestions array
        let randomIndex = Math.floor(Math.random() * availableQuestions.length);
        // Remove the selected question index from availableQuestions and get the corresponding question ID
        let selectedQuestion = blockQuestions[availableQuestions.splice(randomIndex, 1)[0] - 1];
        // Add the selected question ID to the selectedQuestions array
        selectedQuestions.push(selectedQuestion);
    }

    // Randomly select 3 questions from the second block (Q2)
    while (selectedQuestions.length < 6) {
        // Generate a random index from the remaining availableQuestions array
        let randomIndex = Math.floor(Math.random() * availableQuestions.length);
        // Remove the selected question index from availableQuestions and get the corresponding question ID
        // Note: Adding 11 to the index to access Q2 questions (indices 12 to 23 in blockQuestions)
        let selectedQuestion = blockQuestions[availableQuestions.splice(randomIndex, 1)[0] + 11];
        // Add the selected question ID to the selectedQuestions array
        selectedQuestions.push(selectedQuestion);
    }

    // Store the selected questions as embedded data in the Qualtrics survey
    // The questions are joined into a comma-separated string
    Qualtrics.SurveyEngine.setEmbeddedData("SelectedQuestions", selectedQuestions.join(","));
});

// Add an onReady event handler to the Qualtrics survey engine
Qualtrics.SurveyEngine.addOnReady(function() {
    /* Place your JavaScript here to run when the page is fully displayed */
    // This function is executed when the survey page is fully loaded and ready
});

// Add an onUnload event handler to the Qualtrics survey engine
Qualtrics.SurveyEngine.addOnUnload(function() {
    /* Place your JavaScript here to run when the page is unloaded */
    // This function is executed when the survey page is unloaded (e.g., when navigating to the next page)
});