import { mount } from '@vue/test-utils'
import Hello from '@/comments/index/'

describe('HelloWorld', () => {
  test('display Hello World', () => {
    const wrapper = mount(Hello)
    expect(wrapper.text()).toBe("東京都")
  })
})