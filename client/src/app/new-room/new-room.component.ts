import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { Router } from '@angular/router';

import { Tag } from '../models/tag';
import { NewRoomMessage } from './new-room-message';

import { QwizService } from '../qwiz-service/qwiz-service';
import { CreateRoomRequest } from 'app/models/create-room-request';
import { CreateRoomResponse } from 'app/models/create-room-response';
import { QuizService } from '../quiz-service/quiz.service';
import { WsMessage } from '../models/ws-message';

@Component({
  selector: 'app-new-room',
  templateUrl: './new-room.component.html',
  styleUrls: ['./new-room.component.css']
})
export class NewRoomComponent implements OnInit {

  createRoomForm: FormGroup;
  tags: Tag[];
  createRoomResponse: CreateRoomResponse;

  constructor(
    private fb: FormBuilder,
    private router: Router,
    private qwizService: QwizService,
    private quizService: QuizService
  ) {
    this.createRoomForm = this.fb.group({
      roomName: this.fb.control(''),
      topic: this.fb.control(''),
      username: this.fb.control(''),
      numberOfQuestions: this.fb.control('')
    });
  }

  ngOnInit() {
    this.getTags();
  }

  getTags() : void {
    this.qwizService.getTags()
      .subscribe(tags => this.tags = tags);
  }

  createRoom(formValue) {

    let message = new CreateRoomRequest();
    message.name = formValue.roomName;
    message.tags[0] = formValue.topic;
    message.num_questions = formValue.numberOfQuestions;

    this.qwizService.createRoom(message).subscribe(response => 
      {
        this.router.navigate(['waiting', response.code, formValue.username]);
      });
  }

  joinroom(message: WsMessage) {
    this.quizService.registerWithRoom(message);
  }

  home() {
    this.router.navigate(['landing']);
  }

}
