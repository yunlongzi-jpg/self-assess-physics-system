document.addEventListener('DOMContentLoaded', function () {
    let currentQuestion = {};
    let difficulty = 'medium';
    let questionCount = 0;
    const maxQuestions = 10;
    const userId = 'user1';
    const questions = []
    const answers = []
    let score = 0

    let easyMistakes = 0;
    let mediumMistakes = 0;
    let hardMistakes = 0;

    const questionContainer = document.getElementById('question-container');
    const questionText = document.getElementById('question-text');
    const questionImg = document.getElementById('question-img');
    const optionsContainer = document.getElementById('options-container');
    const inputsContainer = document.getElementById('inputs-container');
    const submitButton = document.getElementById('submit-button');
    const reportBody = document.getElementById('report-body');
    const resultsSection = document.getElementById('results-section');
    const explanationContainer = document.getElementById('explanation-container');

    const fetchQuestion = () => {
        fetch(`/question?userId=${userId}&difficulty=${difficulty}`)
            .then(response => response.json())
            .then(data => {
                currentQuestion = data;
                displayQuestion(data);
            });
    }

    const displayQuestion = (question) => {
        questions.push(question)
        questionText.textContent = `【${questionCount + 1}】${question.text}`;
        inputsContainer.innerHTML = '';
        optionsContainer.innerHTML = ''; // Clear previous options
        questionImg.innerHTML = ''; // 清除之前的图片

        // 如果有图片路径，则显示图片
        if (question.img && question.img.length > 0) {
            question.img.forEach(imageName => {
                const imgElement = document.createElement('img');
                imgElement.src = `/static/imgs/${imageName}`;
                imgElement.alt = "";
                imgElement.style.maxWidth = '100%';
                questionImg.appendChild(imgElement);
            });
        }

        if (question.options.length > 0) {
            // 如果有选项，则显示选择题
            question.options.forEach(option => {
                const optionElement = document.createElement('div');
                optionElement.classList.add('option');

                // 判断选项是文本还是图片
                if (option.startsWith('/static/imgs/')) {
                    // 如果选项是图片路径，创建img元素
                    const imgElement = document.createElement('img');
                    imgElement.src = option;
                    imgElement.alt = option;
                    imgElement.style.maxWidth = '100%'; // 限制图片最大宽度
                    optionElement.appendChild(imgElement);
                } else {
                    // 如果选项是文本，直接显示文本
                    optionElement.textContent = option;
                }

                optionsContainer.appendChild(optionElement);

                optionElement.addEventListener('click', () => {
                    document.querySelectorAll('.option').forEach(opt => opt.classList.remove('selected'));
                    optionElement.classList.add('selected');
                });
            });
        } else if (question.answer.length > 0) {
            // 如果没有选项但有答案，则显示填空题
            question.answer.forEach(() => {
                const inputElement = document.createElement('input');
                inputElement.type = 'text';
                inputElement.classList.add('input');
                inputsContainer.appendChild(inputElement);
            });
        } else {
            // 如果既没有选项也没有答案，则显示简答题
            const textAreaElement = document.createElement('textarea');
            textAreaElement.classList.add('input');
            textAreaElement.style.width = '100%';
            textAreaElement.style.height = '100px';
            inputsContainer.appendChild(textAreaElement);
        }
    }

    submitButton.addEventListener('click', function () {
        const selectedOption = document.querySelector('.option.selected');
        const inputElements = document.querySelectorAll('.input');
        let isCorrect = false;
        let userAnswer;

        if (selectedOption) {
            // 处理选择题的逻辑
            const imgElement = selectedOption.querySelector('img');
            if (imgElement) {
                // 处理图片选项的逻辑
                userAnswer = imgElement.alt;
            } else {
                // 处理文本选项的逻辑
                userAnswer = selectedOption.textContent;
            }

            // 检查答案是否正确
            isCorrect = userAnswer === currentQuestion.answer;
        } else if (inputElements.length > 0) {
            // 处理填空题的逻辑
            let allFilled = true; // 确保所有输入框已填写
            let userAnswers = [];

            inputElements.forEach((input) => {
                if (input.value.trim() === '') {
                    allFilled = false; // 发现有未填写的输入框
                }
                userAnswers.push(input.value.trim());
            });

            if (!allFilled) {
                alert('请填写所有的输入框');
                return;
            }

            // 用户答案数组
            userAnswer = userAnswers;
            // 检查填空题答案是否正确
            isCorrect = JSON.stringify(userAnswers) === JSON.stringify(currentQuestion.answer);
        } else {
            // 处理简答题的逻辑（假设简答题只有一个textarea输入框）
            const textareaElement = document.querySelector('textarea.input');
            if (textareaElement && textareaElement.value.trim() === '') {
                alert('请填写您的答案');
                return;
            }
            // 用户的答案
            userAnswer = textareaElement.value.trim();
            // 简答题不计分，直接继续
            questionCount++;
            if (questionCount < maxQuestions) {
                fetchQuestion();
            } else {
                alert('完成所有题目');
                showResults(); // 传入题目和用户答案
            }
            return;
        }

        if (!isCorrect) {
            if (difficulty === 'easy') {
                easyMistakes++
            } else if (difficulty === 'medium') {
                mediumMistakes++
            } else {
                hardMistakes++
            }
        }

        questionCount++;

        // 更新用户的答案
        answers.push(userAnswer);

        // 更新服务器端的分数
        updateScore(userId, difficulty, isCorrect);

        // 根据回答正确性调整下一题的难度
        difficulty = isCorrect ? (difficulty === 'easy' ? 'medium' : 'hard') : (difficulty === 'hard' ? 'medium' : 'easy');

        if (questionCount < maxQuestions) {
            fetchQuestion();
        } else {
            alert('完成所有题目');
            showResults();
        }
    });


    const updateScore = (userId, difficulty, isCorrect) => {
        fetch('/update-score', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                userId: userId,
                difficulty: difficulty,
                isCorrect: isCorrect
            })
        })
            .then(response => response.json())
            .then(() => fetchScores());
    }

    const fetchScores = () => {
        fetch('/scores')
            .then(response => response.json())
            .then(data => updateScoresTable(data));
    }

    const updateScoresTable = (data) => {
        reportBody.innerHTML = ''; // Clear existing table rows

        for (const userId in data) {
            const row = document.createElement('tr');
            const userIdCell = document.createElement('td');
            userIdCell.textContent = userId;
            row.appendChild(userIdCell);

            const easyScoreCell = document.createElement('td');
            easyScoreCell.textContent = `${data[userId].easyTrueCount} / ${data[userId].easyCount}`;
            row.appendChild(easyScoreCell);

            const mediumScoreCell = document.createElement('td');
            mediumScoreCell.textContent = `${data[userId].mediumTrueCount} / ${data[userId].mediumCount}`;
            row.appendChild(mediumScoreCell);

            const hardScoreCell = document.createElement('td');
            hardScoreCell.textContent = `${data[userId].hardTrueCount} / ${data[userId].hardCount}`;
            row.appendChild(hardScoreCell);

            const finalScoreCell = document.createElement('td');
            finalScoreCell.textContent = `${data[userId].easyTrueCount + data[userId].mediumTrueCount + data[userId].hardTrueCount} / ${data[userId].easyCount + data[userId].mediumCount + data[userId].hardCount}`
            row.appendChild(finalScoreCell);

            reportBody.appendChild(row);
        }
    }

    const showResults = () => {
        questionContainer.style.display = 'none';
        submitButton.style.display = 'none';
        resultsSection.style.display = 'block';  // 显示结果部分
        explanationContainer.innerHTML = '';  // 清空之前的解析内容

        questions.forEach((question, index) => {
            const userAnswer = answers[index];
            const correctAnswer = question.answer;
            const isCorrect = JSON.stringify(userAnswer) === JSON.stringify(correctAnswer);

            const resultElement = document.createElement('div');
            resultElement.classList.add('result-item');

            const questionTextElement = document.createElement('p');
            questionTextElement.innerHTML = `<strong>题目${index + 1}:</strong> ${question.text}`;
            resultElement.appendChild(questionTextElement);

            const isCorrectElement = document.createElement('p');
            isCorrectElement.innerHTML = `<strong>正确:</strong> ${isCorrect ? '是' : '否'}`;
            resultElement.appendChild(isCorrectElement);

            const userAnswerElement = document.createElement('p');
            if (typeof userAnswer === 'string' && userAnswer.startsWith('/static/imgs/')) {
                // 如果用户答案是图片路径，则显示图片
                const imgElement = document.createElement('img');
                imgElement.src = userAnswer;
                imgElement.alt = "User Answer Image";
                imgElement.style.maxWidth = '100%';
                userAnswerElement.appendChild(imgElement);
            } else {
                // 否则显示文本答案
                userAnswerElement.innerHTML = `<strong>你的答案:</strong> ${Array.isArray(userAnswer) ? userAnswer.join(', ') : userAnswer}`;
            }
            resultElement.appendChild(userAnswerElement);

            const correctAnswerElement = document.createElement('p');
            if (typeof correctAnswer === 'string' && correctAnswer.startsWith('/static/imgs/')) {
                // 如果正确答案是图片路径，则显示图片
                const imgElement = document.createElement('img');
                imgElement.src = correctAnswer;
                imgElement.alt = "Correct Answer Image";
                imgElement.style.maxWidth = '100%';
                correctAnswerElement.appendChild(imgElement);
            } else {
                // 否则显示文本答案
                correctAnswerElement.innerHTML = `<strong>正确答案:</strong> ${Array.isArray(correctAnswer) ? correctAnswer.join(', ') : correctAnswer}`;
            }
            resultElement.appendChild(correctAnswerElement);

            const explanationTextElement = document.createElement('p');
            explanationTextElement.innerHTML = `<strong>解析:</strong> ${question.analysis}`;
            resultElement.appendChild(explanationTextElement);

            explanationContainer.appendChild(resultElement);
        });

        // 额外解析部分
        const extraQuestion = {
            'id': 19,
            'text': 'To alleviate the traffic congestion between two cities such as Beijing and Guangzhou, engineers have proposed building a rail tunnel along a chord line connecting the cities (Fig. below). A train, unpropelled by any engine and starting from rest, would fall through the first half of the tunnel and then move up the second half. Assuming Earth is a uniform sphere and ignoring air drag and friction, find the city-to-city travel time, expressed by G, the Earth mass M and radius R. (Assume the Earth is with uniform density)',
            'img': ['19.png'],
            'options': [],
            'answer': ['/static/imgs/19-1.png', '/static/imgs/19-2.png', '/static/imgs/20.png'],
            'analysis': 'Ppt 9&11'
        };

        const extraResultElement = document.createElement('div');
        extraResultElement.classList.add('result-item');

        const extraQuestionTextElement = document.createElement('p');
        extraQuestionTextElement.innerHTML = `<strong>额外题目:</strong> ${extraQuestion.text}`;
        extraResultElement.appendChild(extraQuestionTextElement);

        // 显示额外题目的图片
        extraQuestion.img.forEach(imageName => {
            const imgElement = document.createElement('img');
            imgElement.src = `/static/imgs/${imageName}`;
            imgElement.alt = "Extra Question Image";
            imgElement.style.maxWidth = '100%';
            extraResultElement.appendChild(imgElement);
        });

        const extraCorrectAnswerElement = document.createElement('p');
        extraCorrectAnswerElement.innerHTML = `<strong>正确答案:</strong>`;

        extraQuestion.answer.forEach(answerImage => {
            const imgElement = document.createElement('img');
            imgElement.src = answerImage;
            imgElement.alt = "Correct Answer Image";
            imgElement.style.maxWidth = '100%';
            extraCorrectAnswerElement.appendChild(imgElement);
        });

        extraResultElement.appendChild(extraCorrectAnswerElement);

        const extraExplanationTextElement = document.createElement('p');
        extraExplanationTextElement.innerHTML = `<strong>解析:</strong> ${extraQuestion.analysis}`;
        extraResultElement.appendChild(extraExplanationTextElement);

        explanationContainer.appendChild(extraResultElement);

        const maxMistakes = Math.max(easyMistakes, mediumMistakes, hardMistakes);
        const suggestionElement = document.createElement('div');
        const suggestionTitleElement = document.createElement('h2')
        suggestionTitleElement.innerHTML = 'Suggestion'
        explanationContainer.appendChild(suggestionTitleElement)
        if (maxMistakes === easyMistakes) {
            suggestionElement.innerHTML = `<p>Suggestion: Easy questions test basic understanding of core concepts like Newton’s laws, and energy conservation. If students struggle here, it indicates a gap in their fundamental physics knowledge.</p>`
                + `<p>Action Plan: Action Plan: Students should start by identifying the specific concepts they are weak in, then revisit textbook chapters, lecture slides, or video tutorials that explain these topics in depth. Flashcards or summary sheets can help in memorizing key formulas. They should also do targeted practice with simpler problems to build confidence and fluency in applying basic principles.</p>`
                + `<p>Long-term improvement: It’s beneficial to spend 10-15 minutes daily reviewing key formulas and definitions to reinforce basic concepts and ensure long-term retention is beneficial.</p>`
        } else if (maxMistakes === mediumMistakes) {
            suggestionElement.innerHTML = `<p>Suggestion: Medium-level questions typically require applying multiple principles or combining concepts in calculations. Mistakes at this level often stem from difficulty in synthesizing information, such as combining kinematic equations with energy conservation principles.</p>`
                + `<p>Action Plan: Students should focus on reviewing worked-out examples from their notes or textbooks that illustrate these multi-step problems. Breaking down the problem into smaller steps can help improve clarity. Students could benefit from identifying similar problems that combine the same principles and practicing those, slowly increasing the complexity.</p>`
                + `<p>Long-term improvement: Engage in group study sessions where students explain complex problems to one another. Teaching concepts is an effective way to solidify their understanding.</p>`
        } else if (maxMistakes === hardMistakes) {
            suggestionElement.innerHTML = `<p>Suggestion: Difficult questions usually challenge students with more abstract reasoning, unusual applications of principles, or problems involving multiple steps with little guidance. Mistakes at this level suggest the student needs to deepen their problem-solving strategies.</p>`
                + `<p>Action Plan: Students should first revisit foundational concepts to ensure they are completely understood, as these form the basis for solving harder problems. They can work on advanced problems from textbooks or past exams and focus on understanding where they are going wrong by dissecting each mistake. Seeking feedback from professors or TAs is crucial in identifying blind spots.</p>`
                + `<p>Long-term improvement: Developing logical reasoning through puzzles, brainteasers, or research articles can help students become more comfortable thinking critically and creatively when approaching unfamiliar problems.</p>`
        }
        explanationContainer.appendChild(suggestionElement)
        const scoreElement = document.createElement('div')
        const scoreTitleElement = document.createElement('h2')
        scoreTitleElement.innerHTML = 'Score'
        explanationContainer.appendChild(scoreTitleElement)
        const trueCount = maxQuestions - easyMistakes - mediumMistakes - hardMistakes;
        if (trueCount < 6) {
            scoreElement.innerHTML = `<p>Suggestion: There are less than 6 correct questions that suggest that a student has substantial knowledge gaps across different topics. They likely need more time and repetition to fully grasp the material.</p>`
                + `<p>Action Plan: Start by creating a study schedule that dedicates time to revisiting each major topic, focusing especially on areas with the most mistakes. It’s important to go beyond passive review; active techniques like solving problems, summarizing notes, and teaching others can make a big difference. Seeking additional tutoring or attending office hours regularly may also provide more personalized help.</p>`
                + `<p>Long-term improvement: Building consistent study habits will be key to long-term success. Students can benefit from frequent low-stakes quizzes and reviewing notes after each lecture to solidify understanding.</p>`
        } else if (score < 8) {
            scoreElement.innerHTML = `<p>Suggestion: This score range indicates a solid understanding but room for improvement, particularly on more complex or less familiar material.</p>`
                + `<p>Action Plan: Focus on mistakes made in mid-level and advanced problems. Students should engage in more problem-solving practice, especially on harder questions that require synthesis of multiple concepts. They could also benefit from discussing their mistakes with classmates or professors to clarify confusing concepts and correct misunderstandings.</p>`
                + `<p>Long-term improvement: Gradual improvement in handling difficult problems will come from sustained, focused practice. Developing a deeper understanding of the theory behind each concept, rather than just memorizing formulas, will enhance their ability to tackle complex questions.</p>`
        } else {
            scoreElement.innerHTML = `<p>Suggestion: There are more than eight right questions that show excellent comprehension and mastery of the material. However, there is still room for further growth, particularly in exploring more advanced applications of the material.</p>`
                + `<p>Action Plan: These students should aim to challenge themselves by attempting more advanced problems or seeking out additional resources, such as research papers, advanced textbooks, or online physics simulations. Taking part in extra-curricular activities like physics clubs or academic competitions can also offer new challenges and deeper engagement with the subject.</p>`
                + `<p>Long-term improvement: Continuing to seek out and solve new, unfamiliar problems will build greater confidence and flexibility. Encouraging students to apply physics concepts in real-world scenarios or interdisciplinary contexts (e.g., physics in engineering, chemistry, or biology) can further broaden their expertise and analytical skills.</p>`
        }
        explanationContainer.appendChild(scoreElement)
        // 反馈
        const feedbackSection = document.createElement('div');
        feedbackSection.classList.add('feedback-section');

        const feedbackTitle = document.createElement('h2');
        feedbackTitle.textContent = 'Student Feedback';
        feedbackSection.appendChild(feedbackTitle);

        const feedbackTextArea = document.createElement('textarea');
        feedbackTextArea.classList.add('feedback-input');
        feedbackTextArea.style.width = '100%';
        feedbackTextArea.style.height = '100px';
        feedbackTextArea.placeholder = 'Please input your feedback...';
        feedbackSection.appendChild(feedbackTextArea);

        const feedbackSubmitButton = document.createElement('button');
        feedbackSubmitButton.textContent = 'Submit';
        feedbackSection.appendChild(feedbackSubmitButton);
        explanationContainer.appendChild(feedbackSection);

        feedbackSubmitButton.addEventListener('click', () => {
            const feedback = feedbackTextArea.value.trim();
            if (feedback === '') {
                alert('Please input your feedback!');
                return;
            }
            alert('Thanks for your feedback!');
            generatePDFReport(userId, score, scoreElement, feedback);
        });
    }
    const generatePDFReport = async (studentName, score, scoreElement, feedback) => {
        const response = await fetch('/scores');
        const scores = await response.json();
        const {jsPDF} = window.jspdf;
        const pdf = new jsPDF();

        pdf.addImage('/static/imgs/logo.jpg', 'JPEG', 130, 5, 75, 20)

        pdf.setFontSize(18);
        pdf.text(`Student ${userId} Score Report`, 20, 20);

        pdf.setFontSize(14);

        pdf.text(`Easy: ${scores[userId].easyTrueCount} / ${scores[userId].easyCount}`, 20, 40)
        pdf.text(`Medium: ${scores[userId].mediumTrueCount} / ${scores[userId].mediumCount}`, 20, 60)
        pdf.text(`Hard: ${scores[userId].hardTrueCount} / ${scores[userId].hardCount}`, 20, 80)
        pdf.text(`All: ${scores[userId].easyTrueCount + scores[userId].mediumTrueCount + scores[userId].hardTrueCount} / ${scores[userId].easyCount + scores[userId].mediumCount + scores[userId].hardCount}`, 20, 100)

        const comments = pdf.splitTextToSize(scoreElement.textContent, 170);
        pdf.text('Comments:', 20, 120);
        pdf.text(comments, 20, 140);

        const commentsHeight = pdf.getTextDimensions(comments.join('\n')).h;
        const feedbackStartY = 60 + commentsHeight + 10;

        pdf.setFontSize(14);
        pdf.text('Student Feedback:', 20, feedbackStartY + 200);
        pdf.setFontSize(12);
        const feedbackLines = pdf.splitTextToSize(feedback, 170);
        pdf.text(feedbackLines, 20, feedbackStartY + 220);

        const currentTime = new Date();
        const timestamp = currentTime.toISOString().replace(/[:.]/g, '-');
        const fileName = `Exam_Report_${studentName}_${timestamp}.pdf`;

        pdf.save(fileName);
    };

    fetchQuestion();
});

