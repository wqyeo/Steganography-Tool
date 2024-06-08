import getApiHttpRoute from "$lib/getApiHttpRoute";

/**
 * @param {string} fileUUID
 */
export default async function fetchRelatedFiles(fileUUID) {
    const options = {
        method: 'GET',
    };

    const baseApiRoute = getApiHttpRoute()
    const response = await fetch(`${baseApiRoute}/related-files?file_uuid=${fileUUID}`, options)

    const replyJson = await response.json()
    return replyJson;
}