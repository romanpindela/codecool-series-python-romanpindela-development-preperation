const fetchApiGet = (url, callback, errCallback = defaultErrCallback) => {
    fetch(url)
        .then(res => res.json())
        .then(data  => callback(data))
        .catch(() => errCallback())
}

const fetchApiPost = (url, callback, body = {}, errCallback = defaultErrCallback) => {
    fetch(url, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify(body)
    })
        .then(res => res.json())
        .then(data => callback(data))
        .catch(() => errCallback())
}


const fetchApiDelete = (url, callback, body = {}, errCallback = defaultErrCallback) => {
    fetch(url, {
        method: "DELETE",
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify(body)
    })
        .then(res => res.json())
        .then(data => callback(data))
        .catch(() => errCallback())
}

const fetchApiPatch = (url, callback, body = {}, errCallback = defaultErrCallback) => {
    fetch(url, {
        method: "PATCH",
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify(body)
    })
        .then(res => res.json())
        .then(data => callback(data))
        .catch(() => errCallback())
}


const defaultErrCallback = () => console.log("Some error occurred while connecting with API")

export {fetchApiPost, fetchApiGet, fetchApiDelete, fetchApiPatch}