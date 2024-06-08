import getApiHttpRoute from "$lib/getApiHttpRoute";

/**
 * @param {File | Blob} file
 */
export default async function uploadForEncode(file) {
    const formData = new FormData();
    // @ts-ignore
    formData.append('file', file);

    try {
        const baseApiRoute = getApiHttpRoute()
        const response = await fetch(`${baseApiRoute}/upload`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        return data
    } catch (error) {
        console.error('Error:', error);
        return {
            "status": "UNKNOWN_ERROR",
            "message": "Unknown error occured, client should try again..."
        }
    }
};