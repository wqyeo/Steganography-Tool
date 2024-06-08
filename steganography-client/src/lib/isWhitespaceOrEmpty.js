/**
 * @param {string} str
 */
export default function isWhitespaceOrEmpty(str) {
    return !str || /^\s*$/.test(str);
}