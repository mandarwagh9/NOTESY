document.addEventListener('DOMContentLoaded', function() {
    // Upload and analyze file
    document.getElementById('uploadButton').addEventListener('click', function() {
      const fileInput = document.getElementById('fileInput');
      
      if (fileInput.files.length === 0) {
        alert("Please select a file.");
        return;
      }
      
      const file = fileInput.files[0];
      const formData = new FormData();
      formData.append('file', file);
      
      // Show processing message in its dedicated element
      document.getElementById('processing-message').innerText = "Processing...";
      
      fetch('/analyze-notes', {
        method: 'POST',
        body: formData
      })
      .then(response => response.json())
      .then(data => {
        // Clear the processing message and display results
        document.getElementById('processing-message').innerText = "";
        displayResults(data);
      })
      .catch(error => {
        console.error('Error:', error);
        document.getElementById('processing-message').innerText = "Error processing the file.";
      });
    });
    
    // Function to display the results in each section
    function displayResults(data) {
      // Remove the hidden class to show the results section
      document.getElementById('results-section').classList.remove('hidden');
      
      // Update Summary Section
      document.getElementById('summary-content').innerText = data.summary;
      
      // Update Flashcards Section
      const flashcardsContainer = document.getElementById('flashcards-container');
      flashcardsContainer.innerHTML = "";
      data.flashcards.forEach(card => {
        const cardDiv = document.createElement('div');
        cardDiv.classList.add('flashcard');
        
        const innerDiv = document.createElement('div');
        innerDiv.classList.add('flashcard-inner');
        
        const frontDiv = document.createElement('div');
        frontDiv.classList.add('flashcard-front');
        frontDiv.innerText = card.question;
        
        const backDiv = document.createElement('div');
        backDiv.classList.add('flashcard-back');
        backDiv.innerText = card.answer;
        
        innerDiv.appendChild(frontDiv);
        innerDiv.appendChild(backDiv);
        cardDiv.appendChild(innerDiv);
        
        // Toggle flip on click
        cardDiv.addEventListener('click', function() {
          cardDiv.classList.toggle('flipped');
        });
        
        flashcardsContainer.appendChild(cardDiv);
      });
      
      // Update Exam Questions Section
      let examText = "";
      if (Array.isArray(data.questions)) {
        examText = data.questions.join("\n");
      } else {
        examText = data.questions;
      }
      document.getElementById('exam-content').innerText = examText;
    }
    
    // Download Summary as PDF with improved styling
    document.getElementById('download-summary').addEventListener('click', function() {
      const summaryText = document.getElementById('summary-content').innerText;
      const { jsPDF } = window.jspdf;
      const doc = new jsPDF();
      
      // Add a header
      doc.setFont("helvetica", "bold");
      doc.setFontSize(16);
      doc.text("Summary", 10, 15);
      
      // Add content with normal styling
      doc.setFont("helvetica", "normal");
      doc.setFontSize(12);
      doc.text(summaryText, 10, 25, { maxWidth: 190 });
      doc.save("summary.pdf");
    });
    
    // Download Flashcards as PDF with improved styling
    document.getElementById('download-flashcards').addEventListener('click', function() {
      const flashcardsContainer = document.getElementById('flashcards-container');
      let flashcardsText = "";
      flashcardsContainer.querySelectorAll('.flashcard').forEach((card, index) => {
        const question = card.querySelector('.flashcard-front').innerText;
        const answer = card.querySelector('.flashcard-back').innerText;
        flashcardsText += `Flashcard ${index + 1}:\nQ: ${question}\nA: ${answer}\n\n`;
      });
      const { jsPDF } = window.jspdf;
      const doc = new jsPDF();
      
      // Header
      doc.setFont("helvetica", "bold");
      doc.setFontSize(16);
      doc.text("Flashcards", 10, 15);
      
      // Content
      doc.setFont("helvetica", "normal");
      doc.setFontSize(12);
      doc.text(flashcardsText, 10, 25, { maxWidth: 190 });
      doc.save("flashcards.pdf");
    });
    
    // Download Exam Questions as PDF with improved styling
    document.getElementById('download-exam').addEventListener('click', function() {
      const examText = document.getElementById('exam-content').innerText;
      const { jsPDF } = window.jspdf;
      const doc = new jsPDF();
      
      // Header
      doc.setFont("helvetica", "bold");
      doc.setFontSize(16);
      doc.text("Exam Questions", 10, 15);
      
      // Content
      doc.setFont("helvetica", "normal");
      doc.setFontSize(12);
      doc.text(examText, 10, 25, { maxWidth: 190 });
      doc.save("exam_questions.pdf");
    });
  });
  