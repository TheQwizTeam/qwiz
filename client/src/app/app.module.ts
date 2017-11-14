import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatCardModule, MatInputModule, MatButtonModule, MatIconModule, MatListModule } from '@angular/material';

import { AngularMaterialModule } from './angular-material/angular-material.module';
import { AppComponent } from './app.component';
import { LandingComponent } from './landing/landing.component';
import { WaitingComponent } from './waiting/waiting.component';
import { StartGameComponent } from './start-game/start-game.component';
import { QuestionComponent } from './question/question.component';
import { OutcomePageComponent } from './outcome-page/outcome-page.component';
import { SummaryPageComponent } from './summary-page/summary-page.component';
import { QuizService } from './quiz-service/quiz.service';
import { CompleteComponent } from './complete/complete.component';

import { LoggedInGuard } from './logged-in/logged-in.guard';
import { NewRoomComponent } from './new-room/new-room.component';

export const appRoutes: Routes = [
  { path: 'landing', component: LandingComponent },
  { path: 'newroom', component: NewRoomComponent },
  { path: 'waiting/:room/:handle', component: WaitingComponent, canActivate: [LoggedInGuard] },
  { path: 'start', component: StartGameComponent, canActivate: [LoggedInGuard] },
  { path: 'question', component: QuestionComponent, canActivate: [LoggedInGuard] },
  { path: 'outcome', component: OutcomePageComponent, canActivate: [LoggedInGuard] },
  { path: 'summary', component: SummaryPageComponent, canActivate: [LoggedInGuard] },
  { path: 'complete', component: CompleteComponent, canActivate: [LoggedInGuard] },
  { path: '', redirectTo: '/landing', pathMatch: 'full' }
];

@NgModule({
  declarations: [
    AppComponent,
    LandingComponent,
    WaitingComponent,
    StartGameComponent,
    QuestionComponent,
    OutcomePageComponent,
    SummaryPageComponent,
    CompleteComponent,
    NewRoomComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    ReactiveFormsModule,
    HttpModule,
    RouterModule.forRoot(appRoutes),
    BrowserAnimationsModule,
    MatCardModule,
    MatInputModule,
    MatButtonModule,
    MatIconModule,
    MatListModule,
    AngularMaterialModule
  ],
  providers: [
    QuizService,

    LoggedInGuard
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
