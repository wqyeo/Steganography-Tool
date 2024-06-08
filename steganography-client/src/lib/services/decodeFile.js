import getApiHttpRoute from "$lib/getApiHttpRoute";

/**
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
    endKey = "==END=="
) {

    const data = {
        file_uuid: uuid,
        r_bits: redBits,
        g_bits: greenBits,
        b_bits: blueBits,
        secret_key: endKey 
    };

    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    };

    const baseApiRoute = getApiHttpRoute()
    const response = await fetch(`${baseApiRoute}/decode`, options)

    const replyJson = await response.json()
    console.log(`response:`)
    console.log(replyJson)
    return replyJson;
}