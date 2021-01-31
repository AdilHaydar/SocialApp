function hideDiv(param)
{
    param.style.display = 'none'
}


function redirect_to_post(element)
{
window.location = '/post/view/'+element.id
}

const popElement = document.getElementById('popDiv_id')

const htmlElement =  document.getElementsByTagName('html')[0]
htmlElement.addEventListener('click', (element) => {
    const popElement = document.getElementById('popDiv_id')
    if (popElement)
    {
      if (Array.from(element.target.classList).includes('popBtn'))
    {
    const post_id = document.getElementById('post_id_value')
    
    popElement.style.display = 'block'
    const contentElements = document.getElementsByClassName('content')
    const contentElementsLists = Array.from(contentElements)
    contentElementsLists.forEach(item => item.style.filter = 'blur(1px)')
    post_id.value = element.target.id
    return
    }
    else if (popElement.style.display === 'block')
    {
    
    if (element.target.id != 'id_comment_statement' && element.target.id != 'popDiv-content-id' && element.target.id != 'thumbnail_id' && element.target.id != 'comment_form' && element.target.id != 'comment_file_id' )
    {
        const popElement = document.getElementById('popDiv_id')
        popElement.style.display = 'none'
        const contentElements = document.getElementsByClassName('content')
        const contentElementsLists = Array.from(contentElements)
        contentElementsLists.forEach(item => item.style.filter = 'blur(0px)')
    }
    }
    }
    
})

    
    //TODO

    //Yukarıdaki olayı tamamla, ekrana gelen popDiv harici başka bir yere tıklanırsa popDivi kapat, bu fonksiyonda en baştan beri çalışmasın diye birşey yap, mesela popDiv açıldığında aktif olsun fonksiyon. 

    /*function popDiv(element)
    {
    const popElement = document.getElementById('popDiv_id')
    popElement.style.display = 'block'
    const contentElements = document.getElementsByClassName('content')
    const contentElementsLists = Array.from(contentElements)
    contentElementsLists.forEach(item => item.style.filter = 'blur(1px)')

    }*/

var medias = Array.prototype.slice.apply(document.querySelectorAll('audio,video'))
medias.forEach(function(media) {
media.addEventListener('play', function(event) {
    medias.forEach(function(media) {
    if(event.target != media) media.pause()
    })
})
})


const formElement = document.getElementById('post_form')
if (formElement)
{
    formElement.addEventListener('submit', (param) =>{
        const files = Array()
        const inputElement = document.getElementById('files_id')
        const getDatas = document.getElementById('thumbnail_id')
        
        getDatas.childNodes.forEach((item) => {
            files.push(item.src)
        })
        
        const jsonData = { files : files }
        inputElement.value = JSON.stringify(jsonData)
        
        })
}

function readImage(element) {
// Check if the file is an image.
if ((element.files[0].type && element.files[0].type.indexOf('image') === -1) && (element.files[0].type && element.files[0].type.indexOf('video') === -1)) 
{
    //console.log('File is not an image.', element.files[0].type, element.files[0])
    alert("The file is not a video or image type !")
}

const reader = new FileReader();

reader.addEventListener('load', (event) => {
    if ( element.files[0].type.indexOf('image') === 0)
    {
    const imgElement = document.createElement('img')
    const divElement = document.getElementById('thumbnail_id')

    imgElement.title = 'Click for remove'
    imgElement.src = event.target.result
    imgElement.classList.add('show-thumbnail')
    imgElement.id = 'show_id'

    imgElement.onclick = (param) => {
        param.target.remove()
    }

    divElement.insertBefore(imgElement, divElement.childNodes[0])
    }
    else if (element.files[0].type.indexOf('video') === 0)
    {
    const videoElement = document.createElement('video')
    const divElement = document.getElementById('thumbnail_id')

    videoElement.title = 'Click for remove'
    videoElement.src = event.target.result
    videoElement.classList.add('video-js','show-thumbnail')
    videoElement.id = 'show_id'

    videoElement.onclick = (param) => {
        param.target.remove()
    }

    divElement.insertBefore(videoElement, divElement.childNodes[0])
    }
})

reader.readAsDataURL(element.files[0])
}



function set_value(changeEvent)
{
const file_name = document.getElementById('fileLabel')
file_name.textContent = changeEvent.value.split('\\').splice(-1).pop()

if (changeEvent.value)
{
    showImage(src,target)
}
}


function send_tags(param)
{
var statement = document.getElementById('id_statement')
const tags = Array()
const hidden_field = document.getElementById("tags")
const statement_arr = statement.value.split(' ')
statement_arr.forEach((element) => {
    if (element.startsWith('#'))
    {
    tags.push(element)
    }

})
const json_tags = {tags : tags}
hidden_field.value = JSON.stringify(json_tags)

}


function showComment()
{
  const element = document.getElementById('invisible_comment')
  element.style.display = 'block'
}

function hideComment(param)
{
  const element = document.getElementById('comment_form')
  element.style.display = 'none'
}

function readAvatar(element) {
  // Check if the file is an image.
  if ((element.files[0].type && element.files[0].type.indexOf('image') === -1) && (element.files[0].type && element.files[0].type.indexOf('video') === -1)) 
      {
          //console.log('File is not an image.', element.files[0].type, element.files[0])
          alert("The file is not a video or image type !")
      }
  
  const reader = new FileReader();
  reader.addEventListener('load', (event) => {
      
      if ( element.files[0].type.indexOf('image') === 0)
      {
      const imgElement = document.getElementById('show-avatar')
      imgElement.src = event.target.result
      }
     
  })
   reader.readAsDataURL(element.files[0])
  
  }
  

function handleSearch(element)
{
  window.location = element.getAttribute('href')
}

/* jQuery */

var infinite = new Waypoint.Infinite({
    element: $('.infinite-container')[0],
    handler: function(direction) {
    
},
offset: 'bottom-in-view',
onBeforePageLoad: function () {
$('.spinner-border').show();
},
onAfterPageLoad: function () {
$('.spinner-border').hide();
}
});



$(document).ready(function(){
    $("#comment_form").submit(function(e){
      e.preventDefault();

      var serializedData = $(this).serialize();
      $.ajax({
        type : "POST",
        url : "/post/create_comment_ajax/",
        data : serializedData,
        success : function(response){
          $("#comment_form")[0].reset();
        },
        error : function(response){
          if (response.status === 406)
          {
            alert("Comment cannot be blank.")
          }
        }
      });
    });
  });

  
$(document).ready(function(){
    $("#post_form").submit(function(e){
      e.preventDefault();

      var serializedData = $(this).serialize();
      $.ajax({
        type : "POST",
        url : "/post/create_post_ajax/",//"{% url 'post:create_post_ajax' %}", html içerisinde djangodan url bilgisini bu şekile alabiliriz.
        data : serializedData,
        success : function(response){
          $("#post_form")[0].reset();
          $("#thumbnail_id").empty();
        },
        error : function(response){
          if(response.status === 406){
            alert("You can't enter empty post.")
          }
          else
          {
            alert("Somethink went wrong.")
          }
        }
      });
    });
  });

function handleLike(param)
{
  if(param.id.includes('unlike'))
  {
    $.ajax({
      type: "GET",
      url: "/post/unlike/",
      data: {'post_id':param.value},
      success : (response) => {
        var element = document.getElementById('red-heart-'+param.value)
        element.id = "white-heart-"+param.value
        element.style.color = "white"

        var count = document.getElementById('like-count-'+param.value)
        count.textContent = parseInt(count.textContent)-1

        param.id = "like-"+param.value
      },
      error: (response) => {
        alert("Somethink went wrong!")
      }
    })
    
  }
  else
  {
    $.ajax({
      type: "GET",
      url: "/post/like/",
      data: {'post_id':param.value},
      success : (response) => {
        var element = document.getElementById('white-heart-'+param.value)
        element.id = "red-heart-"+param.value
        element.style.color = "red"

        var count = document.getElementById('like-count-'+param.value)
        count.textContent = parseInt(count.textContent)+1

        param.id = "unlike-"+param.value
      },
      error: (response) => {
        if(response.status === 406)
        {
          alert("You already liked this post.")
        }
        else
        {
          alert("Somethink went wrong!")
        }
      }
    })
  }
  
}


function handleFollow(param)
{
  if(param.id.includes('unfollow'))
  {
    $.ajax({
      type: "GET",
      url: "/user/ajax/unfollow/",
      data: {'unfollow':param.value},
      success : (response) => {
        param.id = "follow"
        param.classList.remove('btn-outline-danger')
        param.classList.add('btn-outline-info')
        param.textContent = 'Follow'
      },
      error: (response) => {
        alert("Somethink went wrong!")
      }
    })
    
  }
  else
  {
    $.ajax({
      type: "GET",
      url: "/user/ajax/follow/",
      data: {'follow':param.value},
      success : (response) => {
        param.id = "unfollow"
        param.classList.remove('btn-outline-info')
        param.classList.add('btn-outline-danger')
        param.textContent = 'Unfollow'
      },
      error: (response) => {
        if(response.status === 406)
        {
          alert("You already followed this user.")
        }
        else
        {
          alert("Somethink went wrong!")
        }
      }
    })
  }
  
}
