import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { Router } from '@angular/router';

import { QuizService } from '../quiz-service/quiz.service';

@Component({
  selector: 'app-new-room',
  templateUrl: './new-room.component.html',
  styleUrls: ['./new-room.component.css']
})
export class NewRoomComponent implements OnInit {

  roomForm: FormGroup;

  constructor(
    private fb: FormBuilder,
    private router: Router,
    private quizService: QuizService
  ) {
    this.roomForm = this.fb.group({
      roomName: this.fb.control(''),
      topic: this.fb.control(''),
      handle: this.fb.control('')
    });
  }

  ngOnInit() {
  }

  submit(formValue) {
    console.log(formValue);
    this.quizService.open(formValue);
    this.router.navigate(['waiting', formValue.roomName, formValue.handle]);
  }

  home() {
    this.router.navigate(['landing']);
  }

}
