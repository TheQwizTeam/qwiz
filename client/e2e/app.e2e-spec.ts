import { QuizMonsterClientPage } from './app.po';

describe('quiz-monster-client App', () => {
  let page: QuizMonsterClientPage;

  beforeEach(() => {
    page = new QuizMonsterClientPage();
  });

  it('should display message saying app works', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('app works!');
  });
});
