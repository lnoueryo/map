// -- End: Our Application Code --

// afterEach(() => {
//   // runs after each test block
// })
const baseURL = Cypress.env('baseURL')
beforeEach(() => {
  cy.visit(baseURL)
})
const page = {
  spot: {
    spot: baseURL + '/spot',
    prefecture: '?prefecture_id=13',
    city: '&city_code=13101',
    detail: '/detail/13/13101/1',
     get visit () {
      cy.wait(1000)
      cy.visit(this.spot)
      cy.get('div.item', {timeout: 5000}).eq(0).should('have.text', '東京都')
      cy.wait(1000)
      cy.visit(this.spot + this.prefecture)
      cy.get('div.item', {timeout: 5000}).eq(0).should('have.text', '千代田区')
      cy.wait(1000)
      cy.visit(this.spot + this.prefecture + this.city)
      cy.get('div.item', {timeout: 5000}).eq(0).should('have.text', '東京駅丸の内駅前広場')
      cy.wait(1000)
      // cy.visit(this.spot + this.detail)
      // cy.wait(1000)
    }
  },
  station: {
    station: baseURL + '/station',
    prefecture: '/prefecture',
    prefecture_id: '/13',
    name: '/東京駅',
    company: '?company_id=1',
    line: '&line_id=1',
    detail: '/detail/1',
    get visit () {
      cy.wait(1000)
      cy.visit(this.station)
      cy.get('div.item', {timeout: 5000}).eq(0).should('have.text', '東京都')
      cy.wait(1000)
      cy.visit(this.station + this.prefecture + this.prefecture_id)
      cy.get('div.item', {timeout: 5000}).eq(0).should('have.text', '新橋駅')
      cy.wait(1000)
      const encodedName = encodeURI(this.station + this.prefecture_id + this.name)
      cy.visit(encodedName)
      cy.get('div.station-list', {timeout: 5000}).eq(0).should('have.text', '有楽町駅')
      cy.wait(1000)
      cy.visit(encodedName + this.company)
      cy.get('div.company-name', {timeout: 5000}).eq(0).should('have.text', '駅')
      cy.wait(1000)
      cy.visit(encodedName + this.company + this.line)
      cy.get('div.company-name', {timeout: 5000}).eq(0).should('have.text', '駅')
      cy.wait(1000)
      // cy.visit(encodedName + this.detail)
      // cy.wait(1000)
    }
  },
  prefecture: {
    prefecture: baseURL + '/prefecture',
    prefecture_id: '/13',
    city: '/13101',
    get visit () {
      cy.wait(1000)
      cy.visit(this.prefecture)
      cy.get('div.v-card__title', {timeout: 5000}).eq(0).should('have.text', '東京都')
      cy.wait(1000)
      cy.visit(this.prefecture + this.prefecture_id)
      cy.get('h2.anchor', {timeout: 5000}).eq(0).should('have.text', '千代田区')
      cy.wait(1000)
      cy.visit(this.prefecture + this.prefecture_id + this.city)
      cy.get('h1', {timeout: 5000}).eq(0).should('have.text', '千代田区')
      cy.wait(1000)
    }
  }
}

const index = {
  clickHeaderButton: (eq) => {
    cy.get('#header-bar button').click()
    cy.get('nav').should('have.class', 'v-navigation-drawer--open')
    cy.get('.v-navigation-drawer--open a', {timeout: 5000}).eq(eq).click()
    cy.wait(2000)
  }
}
const spot = {
  clickList: (text) => {
    cy.get('div.item', {timeout: 10000}).eq(0).should('have.text', text).click()
    cy.wait(2000)
  },
  clickMarker: () => {
    cy.get('div.labels.marker-label-event', {timeout: 10000}).eq(0).click({force: true})
    cy.wait(2000)
  },
  inputText: (text) => {
    return cy.get('input[placeholder=観光地を検索]').focus().type(text)
  },
  resetText: () => {
    cy.get('button.mdi-close').click()
  },
  clickInputMenu: () => {
    cy.get('.menu div.list').eq(1).click()
  }
}
const spotDetail = {
  clickSliderButton: () => {
    cy.get('.v-window__next button', {timeout: 10000}).eq(0).click()
  }
}
const station = {
  clickList: (text) => {
    cy.get('div.item', {timeout: 10000}).eq(0).should('have.text', text).click()
    cy.wait(2000)
  },
  clickCompanyLabel: (text) => {
    cy.get('label.company-name', {timeout: 10000}).eq(0).should('have.text', text).click()
    cy.wait(2000)
  },
  clickLineLabel: (text) => {
    cy.get('label.line-name', {timeout: 10000}).eq(0).click()
    cy.wait(2000)
  },
  clickMarker: (eq) => {
    cy.get('div.labels.marker-label-event', {timeout: 10000}).eq(eq).click({force: true})
    cy.wait(2000)
  },
  clickDetailButton: () => {
    cy.get('a#station-detail', {timeout: 10000}).eq(0).click({force: true})
    cy.wait(2000)
    cy.go('back')
  },
  clickBackButton: () => {
    cy.get('a#line', {timeout: 10000}).eq(0).click({force: true})
    cy.wait(2000)
  },
  inputText: (text) => {
    return cy.get('input[placeholder=住所・駅名で検索]').focus().type(text)
  },
  resetText: () => {
    cy.get('button.mdi-close').click()
  },
  clickInputMenu: () => {
    cy.get('.menu div.list').eq(1).click()
  }
}
const prefecture = {
  clickCard: () => {
    cy.get('a.v-card', {timeout: 10000}).eq(0).click()
  }
}
const prefectureDetail = {
  clickTab: (eq) => {
    cy.get('h2.tab', {timeout: 10000}).eq(eq).click()
  },
  openAccordion: (eq) => {
    cy.get('div.price-title', {timeout: 10000}).eq(eq).click()
  },
  closeAccordion: (eq) => {
    cy.get('h2.pointer', {timeout: 10000}).eq(eq).click()
  },
}
// -- Start: Our Cypress Tests --
describe('all pages', () => {
  it('visit', () => {
    page.spot.visit
    page.station.visit
    page.prefecture.visit
  })
})
// // -- Start: Our Cypress Tests --
describe('index', () => {
  it('header', () => {
    index.clickHeaderButton(1)
    cy.go('back')
    index.clickHeaderButton(2)
    cy.go('back')
    index.clickHeaderButton(3)
    index.clickHeaderButton(0)
  })
})
describe('spot', () => {
  beforeEach(() => {
    cy.get('a.v-card').eq(0).click()
  })
  it('clickMarker', () => {
    spot.clickMarker()
  })
  it('search', () => {
    spot.inputText('新宿')
    spot.resetText()
    spot.inputText('新宿').type('{enter}')
    cy.wait(2000)
    cy.get('input[placeholder=観光地を検索]').type('{enter}')
    spot.resetText()
    spot.inputText('新宿')
    cy.wait(2000)
    spot.clickInputMenu()
  })
  it('clickList', () => {
    const textArray = ['東京都', '千代田区', '千代田区', '東京駅丸の内駅前広場']
    textArray.forEach((text, index) => {
      if(index == 2) {
        cy.get('div.title', {timeout: 10000}).eq(0).should('have.text', '千代田区').click()
        cy.wait(2000)
        cy.go('back')
      } else {
        spot.clickList(text)
      }
    });
  })
})
describe('spotDetail', () => {
  beforeEach(() => {
    const detail = baseURL + 'spot/detail/13/13101/1'
    cy.visit(detail)
  })
  it('detail', () => {
    cy.get('div.labels', {timeout: 10000}).eq(0).should('have.text', '東京駅丸の内駅前広場')
    cy.get('div[role=button]', {timeout: 10000}).eq(0).click()
    cy.wait(2000)
    spotDetail.clickSliderButton()
    spotDetail.clickSliderButton()
    cy.wait(2000)
    cy.get('div.chip', {timeout: 10000}).eq(0).click()
    cy.wait(2000)
    cy.go('back')
    cy.get('div.average-score', {timeout: 10000}).eq(0).should('have.text', '4.4')
    cy.get('i.mdi-twitter', {timeout: 10000}).eq(0).should('have.class', 'v-icon')
  })
})
describe('station', () => {
  beforeEach(() => {
    cy.get('a.v-card').eq(1).click()
  })
  it('clickMarker', () => {
    const textArray = ['東京都', '大崎駅', '大崎駅', '']
    textArray.forEach(a => {
      station.clickMarker(0)
      cy.wait(4000)
    });
    station.clickDetailButton()
    station.clickMarker(0)
    station.clickBackButton()
    station.clickMarker(2)
  })
  it('search', () => {
    station.inputText('新宿駅')
    station.resetText()
    station.inputText('新宿駅').type('{enter}')
    cy.wait(2000)
    cy.get('input[placeholder=住所・駅名で検索]').type('{enter}')
    station.resetText()
    station.inputText('東新宿駅')
    cy.wait(2000)
    spot.clickInputMenu()
  })
  it('clickList', () => {
    const textArray = ['東京都', '新橋駅', '東日本旅客鉄道', '山手線']
    textArray.forEach((text, index) => {
      if(index == 2) {
        station.clickCompanyLabel(text)
      } else if(index == 3) {
        station.clickLineLabel()
      } else {
        station.clickList(text)
      }
    });
    cy.get('div.station-list', {timeout: 10000}).eq(1).should('have.text', '有楽町駅').click()
    cy.wait(2000)
  })
})
describe('stationDetail', () => {
  beforeEach(() => {
    const detail = encodeURI(baseURL + 'station/13/大崎駅/detail/12')
    cy.visit(detail)
  })
  it('detail', () => {
    cy.get('div.labels', {timeout: 10000}).eq(0).should('have.text', '大崎駅')
    cy.get('div[role=button]', {timeout: 10000}).eq(0).click()
    cy.wait(2000)
    spotDetail.clickSliderButton()
    spotDetail.clickSliderButton()
    cy.wait(2000)
    cy.get('div.chip', {timeout: 10000}).eq(0).click()
    cy.wait(2000)
    cy.go('back')
    cy.get('div.average-score', {timeout: 10000}).eq(0).should('have.text', '3.7')
    cy.get('i.mdi-twitter', {timeout: 10000}).eq(0).should('have.class', 'v-icon')
  })
})
describe('prefecture', () => {
  beforeEach(() => {
    cy.get('a.v-card').eq(2).click()
    cy.wait(2000)
  })
  it('clickCard', () => {
    prefecture.clickCard()
  })
  it('clickAnchor', () => {
    prefecture.clickCard()
    cy.get('h1').should('have.text', '東京都')
    cy.get('a.anchor', {timeout: 10000}).eq(0).click()
  })
})
describe('prefectureDetail', () => {
  beforeEach(() => {
    const detail = baseURL + 'prefecture/13/13101'
    cy.visit(detail)
    cy.wait(2000)
  })
  it.only('detail', () => {
    cy.get('h1', {timeout: 10000}).eq(0).should('have.text', '千代田区')
    prefectureDetail.clickTab(1)
    prefectureDetail.clickTab(2)
    prefectureDetail.openAccordion(1)
    prefectureDetail.openAccordion(2)
    prefectureDetail.closeAccordion(0)
    prefectureDetail.closeAccordion(1)
  })
})
