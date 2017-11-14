import { Component, OnInit } from '@angular/core';

import { QuizService } from '../quiz-service/quiz.service';

@Component({
  selector: 'app-question',
  templateUrl: './question.component.html',
  styleUrls: ['./question.component.css']
})
export class QuestionComponent implements OnInit {

  question;
  answers;

  constructor(private quizService: QuizService) { }

  ngOnInit() {
    this.question = this.quizService.getCurrentQuestion();
    this.answers = this.quizService.getAnswers();
  }

  submitAnswer(answer: string) {
    console.log(answer);
    this.quizService.chooseAnswer(answer);
  }

}
