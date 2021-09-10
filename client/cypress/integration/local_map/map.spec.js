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
beforeEach(() => {
  cy.visit('http://localhost:3000/')
})

afterEach(() => {
  // runs after each test block
})
// -- Start: Our Cypress Tests --
describe('integration testing for main page', () => {

  it.only('header', () => {
    cy.get('header#header-bar button').click()
    cy.get('nav').should('have.class', 'v-navigation-drawer--open')
  })
})
