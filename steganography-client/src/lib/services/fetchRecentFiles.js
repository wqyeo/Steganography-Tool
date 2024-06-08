import getApiHttpRoute from "$lib/getApiHttpRoute";

export default async function fetchRecentFiles() {

    const options = {
        method: 'GET',
    };

    const baseApiRoute = getApiHttpRoute()
    const response = await fetch(`${baseApiRoute}/latest-files`, options)

    const replyJson = await response.json()
    console.log(`response:`)
    console.log(replyJson)
    return replyJson;
}