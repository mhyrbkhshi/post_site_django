function goToComments() {
    var e = document.getElementById('comment_form')
    e.scrollIntoView()
}    
function like(post_slug) {
    const xhttp = new XMLHttpRequest();
    xhttp.onload = function () {

        let r = JSON.parse(this.response)
        let icon = document.getElementById('heart')
        let likeNumber = document.getElementById('like_number')

        if (r['do'] == 'like') {
            icon.setAttribute('class', 'bi bi-suit-heart-fill') 
            likeNumber.innerHTML = r['likes']

        }else if (r['do'] == 'unlike') {
            icon.setAttribute('class', 'bi bi-suit-heart') 
            likeNumber.innerHTML = r['likes']

        }else if (r['do'] == null){
            alert(r['alert'])
        }
        
    }
    xhttp.open('GET',`/post/${post_slug}/like`);
    xhttp.send();
}

function replay(comment_id) {
    target = event.target 
    var replay_input = document.getElementById('replay_input')
    if (target.id == 'replayed') {
        target.setAttribute('class', 'badge bg-secondary')
        target.setAttribute('id', '')
        replay_input.value = ''
    }else{
        remove_replay = document.getElementById('replayed')
        if (remove_replay){
            remove_replay.setAttribute('class', 'badge bg-secondary')
            remove_replay.setAttribute('id', '')    
        }
        target.setAttribute('class', 'badge bg-primary')
        target.setAttribute('id', 'replayed')
        replay_input.value = comment_id
        replay_text = document.getElementById('comment-text')
        replay_text.scrollIntoView()
    }
}
function delete_comment(comment_pk) {
    target = event.target
    const xhttp = new XMLHttpRequest();
    xhttp.onload = function () {
        let r = JSON.parse(this.response)

        if (r.delete == true) {
            target.parentElement.parentElement.parentElement.remove()
            var num = Number(document.getElementById("comment_number").innerHTML) - 1
            document.getElementById("comment_number").innerHTML = num
        }
        
    }
    xhttp.open('GET',`/comment/${comment_pk}/delete`);
    xhttp.send();
    
}