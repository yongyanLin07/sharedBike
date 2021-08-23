function delete_key(r){
        alert("delete Successfully");
        form=document.getElementById("operation");
        form.action="deleteKeyWords/"+r;
        form.method="post";
        form.submit();
    }