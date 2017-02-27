export function getattr(obj, key, defaultVal) {
    return obj && obj[key] || defaultVal
}

export function partial(fn, args) {
    let self = this
    return function() {
        return fn.call(self, args.concat(this.Arguments, args))
    }
}

export function bool(a) {
    return (a !== false &&
            a !== undefined &&
            a !== 0 &&
            a !== null &&
            a !== '' &&
            a !== {})
}

export function str(a) {
    return a.toString()
}
