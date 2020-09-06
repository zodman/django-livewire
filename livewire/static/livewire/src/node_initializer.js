import { kebabCase, debounce } from '@/util'
import ModelAction from '@/action/model'
import MethodAction from '@/action/method'
import DOMElement from '@/dom/dom_element'
import store from '@/Store'

export default {
    initialize(el, component) {
        if (
            store.initialRenderIsFinished &&
            el.rawNode().tagName.toLowerCase() === 'script'
        ) {
            eval(el.rawNode().innerHTML)
            return false
        }

        el.directives.all().forEach(directive => {
            switch (directive.type) {
                case 'init':
                    this.fireActionRightAway(el, directive, component)
                    break

                case 'model':
                    el.setInputValueFromModel(component)
                    this.attachModelListener(el, directive, component)
                    break

                default:
                    if (store.directives.has(directive.type)) {
                        store.directives.call(
                            directive.type,
                            el.el,
                            directive,
                            component
                        )
                    }

                    this.attachDomListener(el, directive, component)
                    break
            }
        })

        store.callHook('elementInitialized', el, component)
    },

    fireActionRightAway(el, directive, component) {
        const method = directive.value ? directive.method : '$refresh'

        component.addAction(new MethodAction(method, directive.params, el))
    },

    attachModelListener(el, directive, component) {
        // This is used by morphdom: morphdom.js:391
        el.el.isLivewireModel = true

        const isLazy = directive.modifiers.includes('lazy')
        const debounceIf = (condition, callback, time) => {
            return condition
                ? component.modelSyncDebounce(callback, time)
                : callback
        }
        const hasDebounceModifier = directive.modifiers.includes('debounce')

        store.callHook(
            'interceptWireModelAttachListener',
            el,
            directive,
            component,
            debounceIf
        )

        // File uploads are handled by UploadFiles.js.
        if (
            el.rawNode().tagName.toLowerCase() === 'input' &&
            el.rawNode().type === 'file'
        )
            return

        const event =
            el.rawNode().tagName.toLowerCase() === 'select' ||
            ['checkbox', 'radio'].includes(el.rawNode().type) ||
            directive.modifiers.includes('lazy')
                ? 'change'
                : 'input'

        // If it's a text input and not .lazy, debounce, otherwise fire immediately.
        let handler = debounceIf(
            hasDebounceModifier || (el.isTextInput() && !isLazy),
            e => {
                const model = directive.value
                const el = new DOMElement(e.target)
                // We have to check for typeof e.detail here for IE 11.
                const value =
                    e instanceof CustomEvent &&
                    typeof e.detail != 'undefined' &&
                    typeof window.document.documentMode == 'undefined'
                        ? e.detail
                        : el.valueFromInput(component)

                component.addAction(new ModelAction(model, value, el))
            },
            directive.durationOr(150)
        )

        el.addEventListener(event, handler)

        component.addListenerForTeardown(() => {
            el.removeEventListener(event, handler)
        })
    },

    attachDomListener(el, directive, component) {
        switch (directive.type) {
            case 'keydown':
            case 'keyup':
                this.attachListener(el, directive, component, e => {
                    // Detect system modifier key combinations if specified.
                    const systemKeyModifiers = [
                        'ctrl',
                        'shift',
                        'alt',
                        'meta',
                        'cmd',
                        'super',
                    ]
                    const selectedSystemKeyModifiers = systemKeyModifiers.filter(
                        key => directive.modifiers.includes(key)
                    )

                    if (selectedSystemKeyModifiers.length > 0) {
                        const selectedButNotPressedKeyModifiers = selectedSystemKeyModifiers.filter(
                            key => {
                                // Alias "cmd" and "super" to "meta"
                                if (key === 'cmd' || key === 'super')
                                    key = 'meta'

                                return !e[`${key}Key`]
                            }
                        )

                        if (selectedButNotPressedKeyModifiers.length > 0)
                            return false
                    }

                    // Strip 'debounce' modifier and time modifiers from modifiers list
                    let modifiers = directive.modifiers.filter(modifier => {
                        return (
                            !modifier.match(/^debounce$/) &&
                            !modifier.match(/^[0-9]+m?s$/)
                        )
                    })

                    // Only handle listener if no, or matching key modifiers are passed.
                    return (
                        modifiers.length === 0 ||
                        modifiers.includes(kebabCase(e.key))
                    )
                })
                break
            case 'click':
                this.attachListener(el, directive, component, e => {
                    // We only care about elements that have the .self modifier on them.
                    if (!directive.modifiers.includes('self')) return

                    // This ensures a listener is only run if the event originated
                    // on the elemenet that registered it (not children).
                    // This is useful for things like modal back-drop listeners.
                    return el.isSameNode(e.target)
                })
                break
            default:
                this.attachListener(el, directive, component)
                break
        }
    },

    attachListener(el, directive, component, callback) {
        if (directive.modifiers.includes('prefetch')) {
            el.addEventListener('mouseenter', () => {
                component.addPrefetchAction(
                    new MethodAction(directive.method, directive.params, el)
                )
            })
        }

        const event = directive.type
        const handler = e => {
            if (callback && callback(e) === false) {
                return
            }

            component.callAfterModelDebounce(() => {
                const el = new DOMElement(e.target)

                directive.setEventContext(e)

                // This is outside the conditional below so "wire:click.prevent" without
                // a value still prevents default.
                this.preventAndStop(e, directive.modifiers)
                const method = directive.method
                let params = directive.params

                if (
                    params.length === 0 &&
                    e instanceof CustomEvent &&
                    e.detail
                ) {
                    params.push(e.detail)
                }

                // Check for global event emission.
                if (method === '$emit') {
                    component.scopedListeners.call(...params)
                    store.emit(...params)
                    return
                }

                if (method === '$emitUp') {
                    store.emitUp(el, ...params)
                    return
                }

                if (method === '$emitSelf') {
                    store.emitSelf(component.id, ...params)
                    return
                }

                if (method === '$emitTo') {
                    store.emitTo(...params)
                    return
                }

                if (directive.value) {
                    component.addAction(new MethodAction(method, params, el))
                }
            })
        }

        const debounceIf = (condition, callback, time) => {
            return condition ? debounce(callback, time) : callback
        }

        const hasDebounceModifier = directive.modifiers.includes('debounce')
        const debouncedHandler = debounceIf(
            hasDebounceModifier,
            handler,
            directive.durationOr(150)
        )

        el.addEventListener(event, debouncedHandler)

        component.addListenerForTeardown(() => {
            el.removeEventListener(event, debouncedHandler)
        })
    },

    preventAndStop(event, modifiers) {
        modifiers.includes('prevent') && event.preventDefault()

        modifiers.includes('stop') && event.stopPropagation()
    },
}
