# DOCUMENTATION OF ROUTING, ROUTING DIAGRAM

![routing-diagram](https://github.com/wqyeo/LSB-Steganography/assets/25131995/dd48091a-4afc-4f13-99ac-d6f19b238959)

> Last updated `v1.0.1`

## Uploading Image `/encode-upload`

Use this route for uploading an image. It should be the first step in the system.<br>It will generate a `uuid`, which **you should keep a reference to it in the client side.**

> Yea, despite the name, just send all images here. Decoding or encoding.

#### Inputs
**POST** Request, form data.

- `file`: [`File`](https://developer.mozilla.org/en-US/docs/Web/API/File)

#### Outputs

- `status: string`; `"SUCCESS"` if the file is valid. Otherwise, it will output other statuses.
- `message: string`; More information tied to the status. If you are lazy, this can work as a error message printed to the user.
- `uuid: string`; **STORE THIS**, you will need this for future API calls related to the image.<br>_(This field only exists when `status == "SUCCESS"`)_

## Get Uploaded Image `/get-uploaded-file/<uuid>`

#### Inputs
**GET** Request.

- `uuid`: `string`; Should already be part of the query URL

#### Outputs

- The path to the image itself. The user can use this URL to download the image. Sends a standard JSON `status` with error if not found.

## Encode a file `/encode-file/<uuid>`

#### Inputs
**POST** Request, JSON data.

- `uuid`: `string`; Should already be part of the query URL
- `r_bits`: `number[]`; Represents the bits (0~7) to use in the red alpha channel.
- `g_bits`: `number[]`; Represents the bits (0~7) to use in the green alpha channel.
- `b_bits`: `number[]`; Represents the bits (0~7) to use in the blue alpha channel.

#### Outputs

- The path to the image itself. The user can use this URL to download the image. Sends a standard JSON `status` with error if not found.

## Get Uploaded Image `/get-uploaded-file/<uuid>`

#### Inputs
**GET** Request, form data.

- `uuid`: `string`; Should already be part of the query URL

#### Outputs

- The path to the image itself. The user can use this URL to download the image. Sends a standard JSON `status` with error if not found.


