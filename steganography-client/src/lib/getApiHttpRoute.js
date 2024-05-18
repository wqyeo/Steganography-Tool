const { VITE_API_DOMAIN, VITE_SSL_ENABLED } = import.meta.env;

/**
 * @returns {string} The base HTTP Route to API, accounted for with SSL or not; Does not come with the trailing backslash '/'.
 */
export default function getApiHttpRoute() {
    return "http://localhost:8080"
}