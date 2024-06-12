import getApiHttpRoute from "$lib/getApiHttpRoute";

/**
 * For images; For picture check 'decodeAudio' function.
 * @param {string} uuid
 * @param {number[]} redBits
 * @param {number[]} greenBits
 * @param {number[]} blueBits
 */
export default async function decodeFile(
    uuid,
    redBits,
    greenBits,
    blueBits,
    endKey = "==END==",
    generatorType = "linear"
) {

    const formData = new FormData();
    formData.append('file_uuid', uuid);
    formData.append('r_bits', JSON.stringify(redBits));
    formData.append('g_bits', JSON.stringify(greenBits));
    formData.append('b_bits', JSON.stringify(blueBits));
    formData.append('secret_key', endKey);
    formData.append('generator_type', generatorType)
    
    const options = {
        method: 'POST',
        body: formData
    };

    const baseApiRoute = getApiHttpRoute()
    const response = await fetch(`${baseApiRoute}/decode`, options)

    const replyJson = await response.json()
    return replyJson;
}