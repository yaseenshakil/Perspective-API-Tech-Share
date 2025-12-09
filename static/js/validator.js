let index = 0;

validationForm = document.getElementById('validation-form');
validationForm.addEventListener('submit', async function(event){
    event.preventDefault();

    const textToValidate = document.getElementById("demo-text-input").value;

    const res = await fetch("/validate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ comment: textToValidate }),
    });

    const data = await res.json();  

    console.log(`success: ${data.success}`)

    console.log("Full response:", data.attributeScores);

    let scores_table = document.getElementById('scores-table')
    scores_table.innerHTML = ""
    for (const key in data.attributeScores){
        var row = scores_table.insertRow();
        var cell1 = row.insertCell(0);
        var cell2 = row.insertCell(1);
        cell1.innerHTML = key;
        cell2.innerHTML = `${(data.attributeScores[key].spanScores[0]?.score?.value * 100.0).toFixed(3)}%`;
    }
});


function generateRandomComment(){
    const spanElement = document.getElementById('random-comment-span');
    var comments = ["Science, Bitch -Jessie, Breaking Bad", "I'm surrounded by Idiots -Scar, Lion King", "I hate everything you chose to be - Michael Scott, The Office", "I am the danger - Walter White, Breaking Bad", "Your mother was a hamster - Monty Python", "I will find you and I will kill you - Bryan Mills, Taken", "You are a worse psychiatrist than you are a son-in-law -Lucille Bluth, Arrested Development"]
    index >= comments.length ? index = 0 : index
    spanElement.innerHTML = comments[index];
    index++;
}