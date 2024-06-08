import getApiHttpRoute from "$lib/getApiHttpRoute";

/**
 * @param {string} uuid
 * @param {number} lsbSelection
 */
export default async function decodeAudio(
    uuid,
    lsbSelection,
    endKey = "==END=="
) {

    const formData = new FormData();
    formData.append('file_uuid', uuid);
    formData.append('lsb_count', lsbSelection.toString());
    formData.append('secret_key', endKey);
    
    const options = {
        method: 'POST',
        body: formData
    };

    const baseApiRoute = getApiHttpRoute()
    const response = await fetch(`${baseApiRoute}/decode`, options)

    const replyJson = await response.json()
    return replyJson;
}