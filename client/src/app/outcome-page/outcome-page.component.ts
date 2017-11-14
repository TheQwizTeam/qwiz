import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { QuizService } from '../quiz-service/quiz.service';

@Component({
  selector: 'app-outcome-page',
  templateUrl: './outcome-page.component.html',
  styleUrls: ['./outcome-page.component.css']
})
export class OutcomePageComponent implements OnInit {

  question;
  chosenAnswer;
  correctAnswer;
  peopleToAnswer;

  constructor(private router: Router,
    private quizService: QuizService) { }

  ngOnInit() {
    this.question = this.quizService.getCurrentQuestion();
    this.chosenAnswer = this.quizService.getChosenAnswer();
    this.correctAnswer = this.quizService.getCorrectAnswer();
  }

  nextQuestion() {
    this.quizService.getNextQuestion();
  }

  testSummaryResponse() {
    this.quizService.testSummaryResponse();
  }

}
