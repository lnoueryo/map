import { mount } from '@vue/test-utils'
import Index from '@/pages/index'
import assert from 'assert'
describe('Index', () => {
  test('display Hello World', () => {
    const wrapper = mount(Index)
    // expect(wrapper.text()).toBe("東京都")
    assert(wrapper.vm.smp === true)
  })
})