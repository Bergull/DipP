$(document).ready(function() {
    imageDict = {}
    imageList = []
    let output = document.getElementById("output")
    
    document.getElementById("upload").addEventListener("change", function(e) {
      let fileInput = document.getElementById('upload');
      if(fileInput.files.length > 0){
        let filename = fileInput.files[0].name.split('.')[0];
        let newImg = new Image(300, 300);
        
        imageDict[filename] = e.target.files[0]
        imageList.push(e.target.files[0])
    
        newImg.src = e.target.files[0];
        newImg.src = URL.createObjectURL(e.target.files[0]);
        
    	let newImgContainer = document.createElement("div");
        newImgContainer.setAttribute("id", filename);
        let rmvBtn = document.createElement("button");
        rmvBtn.setAttribute("class", filename);
        rmvBtn.innerHTML = "Odstranit"
        rmvBtn.onclick = function(e){
        	//console.log(e)
            $("#" + e.target.className).remove()
            console.log( "#" +  e.target.className)
            delete imageDict[e.target.className]
            console.log(imageDict)
        }
        
        //$("#upload").attr("id", filename);
        //$("#offerform").append()
        //$('<input type="file" class = "upload" />').appendTo($("#offerform"))
        
        newdiv = document.createElement("div")
        
        newImgContainer.appendChild(rmvBtn);
        newImgContainer.appendChild(newImg);
        newImgContainer.appendChild(newdiv);
        output.appendChild(newImgContainer);
        //console.log(imageDict)
      }
      });
      $("#offerform").submit(function(e){
          e.preventDefault()
          //$("#hiddenfiles").prop("files", imageList);
          var form = $("#offerform")[0]
          let formData = new FormData(form);
          //var fd = new FormData();
          
          
          /*imageList.forEach(function (item, index){
          //console.log(file)
            //console.log(imageDict[file])
            console.log(item)
            formData.append(item.name, item)    
          })*/
        for(file in imageDict){
            //console.log(file)
            //console.log(imageDict[file])
            formData.append(file, imageDict[file])
        }
            
          for (var key of formData.entries()) {
            console.log(key);
            }
           $.ajax({
            url: '/postoffer/',
            type: 'post',
            data: formData,
            processData: false,
            contentType: false,
            success : function(response){
                console.log(response);
                console.log(response.redirect);
                if(response.redirect){
                    window.location.replace("/imgtest/" + response.redirect);
                }
            }
            })
      })


      
      
      $("#submitimages").click(function(){

        var fd = new FormData();
        for(file in imageDict){
            //console.log(file)
            //console.log(imageDict[file])
            fd.append(file, imageDict[file])
        }
        for (var key of fd.entries()) {
            console.log(key);
        }
        
        $.ajax({
            url: '/receive/',
            type: 'post',
            data: fd,
            processData: false,
            contentType: false,
            success: function(response){
                if(response != 0){
                    alert('something happened')
                    console.log(response)
                    for(prediction in response.predictions){
                        //console.log(prediction);
                        //console.log(response.predictions[prediction]);
                        obj = response.predictions[prediction]
                        //console.log($("#" + prediction));
                    }
                    for(pclass in response.predClasses){
                        console.log("pclass" + pclass)
                        console.log( $("#" + pclass))
                        $("#" + pclass).children("div").eq(0).text(response.predClasses[pclass])
                        //$("#" + pclass).append("<div>" + response.predClasses[pclass] +  "</div>")
                    }
                }else{
                    alert('file not uploaded');
                }
            },
            error: function (response) {
                console.log(response)
            }
        });
    });
})