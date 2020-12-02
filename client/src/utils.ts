export const http = (url: string): Promise<Response> => {
  return new Promise((resolve, reject) => {
    fetch(url, {
      method: "GET",
      credentials: "omit",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
    })
      .then((response: Response) => {
        if (response.ok) {
          resolve(response);
        } else {
          if (response.status != 200) {
            reject(response);
          } else {
            resolve(response);
          }
        }
      })
      .catch((error) => reject(error));
  });
};
