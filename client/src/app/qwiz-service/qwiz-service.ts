import { Injectable } from '@angular/core';
import { environment } from "../../environments/environment";

import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/map'
import { catchError, map, tap } from 'rxjs/operators';
import { of } from 'rxjs/observable/of';

import { Tag } from '../models/tag';
import { TagsResponse } from '../models/tags-response';
import { CreateRoomRequest } from '../models/create-room-request';
import { CreateRoomResponse } from '../models/create-room-response';
import { NewRoomMessage } from 'app/new-room/new-room-message';

@Injectable()
export class QwizService {

  constructor(
    private http: HttpClient
  ) {}

  private tagsUrl = environment.qwizServiceUrl +  'api/tags/';
  private roomUrl = environment.qwizServiceUrl +  'api/room/';

  getTags() : Observable<Tag[]> {

    let headers = new HttpHeaders();
    headers = headers.append("Content-Type", "application/json");

    return this.http.get<TagsResponse>(this.tagsUrl, { headers: headers} )
      .map(resp => resp.results)
  }

  createRoom(createRoomRequest: CreateRoomRequest) : Observable<CreateRoomResponse> {
    let headers = new HttpHeaders();
    headers = headers.append("Content-Type", "application/json");

    console.log(createRoomRequest);
    return this.http.post<CreateRoomResponse>(this.roomUrl, createRoomRequest, { headers: headers });
  }

  private handleError<T> (operation = 'operation', result?: T) {
    return(error: any): Observable<T> => {
      console.error(error);
      this.log(`${operation} failed: ${error.message}`);

      return of(result as T);
    }
  }

  private log(message: string) {
    console.log('Qwiz Service: ' + message);
  }

}
