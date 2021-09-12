// -- Start: Our Application Code --
function fizzbuzz(num) {
  if (num % 3 === 0 && num % 5 === 0) {
    return 'fizzbuzz'
  }

  if (num % 3 === 0) {
    return 'fizz'
  }

  if (num % 5 === 0) {
    return 'buzz'
  }
}
// -- End: Our Application Code --
beforeEach(async() => {
  cy.visit('https://tokyo-map.jpn.org/')
  // await cy.waitUntil(() => cy.window().then(win => true), {
  //   errorMsg: 'This is a custom error message', // overrides the default error message
  //   timeout: 2000, // waits up to 2000 ms, default to 5000
  //   interval: 500 // performs the check every 500 ms, default to 200
  // });
})
afterEach(() => {
  // runs after each test block
})
// -- Start: Our Cypress Tests --
describe('integration testing for main page', () => {

  it.only('header', () => {
    cy.get('#header-bar button').click()
    cy.get('nav').should('have.class', 'v-navigation-drawer--open')
  })
})
