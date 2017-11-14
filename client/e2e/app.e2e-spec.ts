import { QwizClientPage } from './app.po';

describe('qwiz-client App', () => {
  let page: QwizClientPage;

  beforeEach(() => {
    page = new QwizClientPage();
  });

  it('should display message saying app works', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('app works!');
  });
});
