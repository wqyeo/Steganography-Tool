import getApiHttpRoute from "$lib/getApiHttpRoute";

/**
 * @param {string} uuid
 * @param {number} lsbSelection
 * @param {string} toEncode
 */
export default async function encodeAudio(
    uuid,
    toEncode,
    lsbSelection,
    endKey = "==END=="
) {

    const formData = new FormData();
    formData.append('file_uuid', uuid);
    formData.append('lsb_count', lsbSelection.toString());
    formData.append('message', toEncode);
    formData.append('secret_key', endKey);

    const options = {
        method: 'POST',
        body: formData
    };

    const baseApiRoute = getApiHttpRoute()
    const response = await fetch(`${baseApiRoute}/encode`, options)

    const replyJson = await response.json()
    return replyJson;
}