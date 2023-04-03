document.getElementById("displaytext").style.display = "none";

function searchPhoto() {

  var apigClient = apigClientFactory.newClient({
    apiKey: 'gnavV2E0Pz5Kit0HSnfqL8loqijjhvHH7gZTVV9Z'
  });
  console.log("Client created");
  var image_message = document.getElementById("note-textarea").value;
  if(image_message == "")
    var image_message = document.getElementById("transcript").value;

  console.log(image_message);

  var body = {};
  var params = {
    q: image_message,
    'x-api-key': 'gnavV2E0Pz5Kit0HSnfqL8loqijjhvHH7gZTVV9Z'
  };
  var additionalParams = {
    headers: {
      'Content-Type': "application/json",
      // "Access-Control-Allow-Credentials": "true",
      // // "Access-Control-Allow-Methods": "GET,HEAD,OPTIONS,POST,PUT",
      // 'Access-Control-Allow-Headers': 'Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers, Methods',
      // 'Access-Control-Allow-Origin': '*',
    },
  };

  apigClient.searchGet(params, body, additionalParams)
    .then(function (result) {
      //This is where you would put a success callback
      console.log("Inside searchGet");
      console.log(result);
      response_data = result.data
      console.log(response_data);
      var img1 = [result.data.results[0].url];
      console.log("BODY!");
      console.log(img1);
      length_of_response = img1.length;
      console.log(length_of_response);
      if (length_of_response == 0) {
        document.getElementById("displaytext").innerHTML = "No Images Found !!!"
        document.getElementById("displaytext").style.display = "block";
      }

      // img1 = img1.replace(/\"/g, "").replace("[", "").replace("]", "");
      // img1 = img1.split(",");

      document.getElementById("img-container").innerHTML = "";
      var para = document.createElement("p");
      para.setAttribute("id", "displaytext")
      document.getElementById("img-container").appendChild(para);
      

      img1.forEach(function (obj) {
        var img = new Image();
        console.log("Inside forEach");
        console.log(obj);
        // img.src = "https://photosforsearch1.s3.amazonaws.com/"+obj;
        img.src = obj;
        img.setAttribute("class", "banner-img");
        img.setAttribute("alt", "effy");
        img.setAttribute("width", "150");
        img.setAttribute("height", "100");
        document.getElementById("displaytext").innerHTML = "Images returned are : "
        document.getElementById("img-container").appendChild(img);
        document.getElementById("displaytext").style.display = "block";

      });
    }).catch(function (result) {
      //This is where you would put an error callback
    });

}

function getBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    // reader.onload = () => resolve(reader.result)
    reader.onload = () => {
      let encoded = reader.result.replace(/^data:(.*;base64,)?/, '');
      if ((encoded.length % 4) > 0) {
        encoded += '='.repeat(4 - (encoded.length % 4));
      }
      resolve(encoded);
    };
    reader.onerror = error => reject(error);
  });
}

function uploadPhoto() {
  // var file_data = $("#file_path").prop("files")[0];
  var body = document.getElementById('file_path').files[0];
  console.log("Starting upload");
  console.log(body);
  const reader = new FileReader();

  var apigClient = apigClientFactory.newClient({
          apiKey: "gnavV2E0Pz5Kit0HSnfqL8loqijjhvHH7gZTVV9Z",
          defaultContentType: "image/jpeg",
          defaultAcceptType: "image/jpeg"
        });

  var params = {
    "key": body.name,
    "bucket":"cloud-photos-b2",
    // "folder": "photosforsearch1",
    // 'x-api-key': 'gnavV2E0Pz5Kit0HSnfqL8loqijjhvHH7gZTVV9Z'
  };

      //   var additionalParams = {
      //   headers: {
      //     'Content-Type': "image/jpeg",
      //     // 'Access-Control-Allow-Headers': 'Content-Type, Origin',
      //     // 'Access-Control-Allow-Origin': '*',
      //     // 'Access-Control-Allow-Methods': '*',
      //   },
      // };


  apigClient.uploadPut(params, body).then(function (res) {
    if (res.status == 200) {
      // alert("Upload Successfull")
      console.log("Success");
      document.getElementById("uploadText").innerHTML = "IMAGE UPLOADED SUCCESSFULLY !!!"
      document.getElementById("uploadText").style.display = "block";
      document.getElementById("uploadText").style.color = "green";
      document.getElementById("uploadText").style.fontWeight = "bold";
    }
  });
  // var file = document.querySelector('#file_path > input[type="file"]').files[0];
  // var encoded_image = getBase64(file).then(
  //   data => {
  //     // console.log(data)
  //     var apigClient = apigClientFactory.newClient({
  //       apiKey: "gnavV2E0Pz5Kit0HSnfqL8loqijjhvHH7gZTVV9Z",
  //       defaultContentType: "image/jpeg",
  //       defaultAcceptType: "image/jpeg"
  //     });

  //     // var data = document.getElementById('file_path').value;
  //     // var x = data.split("\\")
  //     // var filename = x[x.length-1]
  //     //  var file_type = file.type + ";base64"

  //     // var body = data;
  //     var body = file;
  //     var params = {
  //       "key": file.name,
  //       "bucket":"cloud-photos-b2",
  //       // "folder": "photosforsearch1",
  //       'x-api-key': 'gnavV2E0Pz5Kit0HSnfqL8loqijjhvHH7gZTVV9Z'
  //     };

  //     var additionalParams = {
  //       headers: {
  //         'Content-Type': "image/jpeg",
  //         // 'Access-Control-Allow-Headers': 'Content-Type, Origin',
  //         // 'Access-Control-Allow-Origin': '*',
  //         // 'Access-Control-Allow-Methods': '*',
  //       },
  //     };

  //     apigClient.uploadBucketKeyPut(params, body, additionalParams).then(function (res) {
  //       if (res.status == 200) {
  //         // alert("Upload Successfull")
  //         console.log("Success");
  //         document.getElementById("uploadText").innerHTML = "IMAGE UPLOADED SUCCESSFULLY !!!"
  //         document.getElementById("uploadText").style.display = "block";
  //         document.getElementById("uploadText").style.color = "green";
  //         document.getElementById("uploadText").style.fontWeight = "bold";
  //       }
  //     })
  //   });

  
  // let config = {
  //      headers: { 'Content-Type': file.type }
  //  };
  //  url = 'https://cors-anywhere.herokuapp.com/https://q6mpc0sjz1.execute-api.us-east-1.amazonaws.com/TestAuth/upload/photosforsearch1/' + file.name
  //  axios.put(url, file, config).then(response => {
  //   //  console.log(" New "+response.data)
  //   //  alert("Image uploaded successfully!");
  //    console.log("Success");
  //    document.getElementById("uploadText").innerHTML = "IMAGE UPLOADED SUCCESSFULLY !!!"
  //    document.getElementById("uploadText").style.display = "block";
  //    document.getElementById("uploadText").style.color = "green";
  //    document.getElementById("uploadText").style.fontWeight = "bold";
  //  });

}