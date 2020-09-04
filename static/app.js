const form = document.querySelector('#form_guess');
const input = document.querySelector('#search_input');
const guesses = [];
let $count = 1;
let $timer = 30;
let $score = 0;
document.getElementById('scoreboard').innerHTML = 'Score: ' + $score;
document.getElementById('timer').innerHTML = 'Timer: ' + $timer;

async function get_word_attempt(guess) {
	const resp = await axios.get('/check-word', { params: { word: guess } });
	//let $search_term = guess;
	//console.log($search_term);
	//console.log(resp.data['result']);

	if ((resp.data['result'] === 'ok') & (guesses.indexOf(guess) === -1)) {
		//console.log('you got it');
		$('#guesswordslist').append(`<li class="guesses correct">${guess}</li>`);
		$('#scoredwordslist').append(`<li class="correct">${guess}</li>`);
		guesses.push(guess);
		$score = $score + guess.length;
		document.getElementById('scoreboard').innerHTML = 'Score: ' + $score;
	}
	else if (resp.data['result'] === 'ok') {
		//console.log('made it to duplicate loop');
		if (guesses.indexOf(guess) !== -1) {
			//console.log('duplicate!');
			let $duplicate = $(`<div class="alert alert-warning alert-dismissible fade show text-center" role="alert">
			<strong>${guess} : </strong> has already been used!!  ლ(▀̿̿Ĺ̯̿̿▀̿ლ)
			<button type="button" class="close" data-dismiss="alert" aria-label="Close">
			  <span aria-hidden="true">&times;</span>
			</button>
		  </div>`);
			$('#wrong').append($duplicate);
		}
	}
	else if (resp.data['result'] === 'not-on-board') {
		//console.log('not on board');
		$('#guesswordslist').append(`<li class="not_on_board">${guess}</li>`);
		guesses.push(guess);
	}
	else {
		let $wrong = $(`<div class="alert alert-danger alert-dismissible fade show text-center" role="alert">
		<strong>${guess} : </strong>That happens to not be a word (つ☢益☢)つ︵┻━┻
		<button type="button" class="close" data-dismiss="alert" aria-label="Close">
		  <span aria-hidden="true">&times;</span>
		</button>
	  </div>`);
		$('#wrong').append($wrong);
		//console.log('not-word');
	}
}

form.addEventListener('submit', function(e) {
	e.preventDefault();
	get_word_attempt(input.value);
	input.value = '';
});

let decreaseTime = setInterval(function() {
	$timer = $timer - 1;
	document.getElementById('timer').innerHTML = 'Timer: ' + $timer;
	if ($timer < 1) {
		document.getElementById('timer').innerHTML = 'Expired!';
		document.getElementById('search_input').outerHTML =
			'<input class="form-control form-control-lg" type="text" placeholder="Game Over" id="search_input" disabled>';
		document.getElementById('submission').outerHTML =
			'<button type="submit" class="btn btn-outline-elegant" id="submission" disabled>Game Over!</button>';
		createReset();
	}
}, 1000);

function createReset() {
	if ($count === 1) {
		let $resetBtn = $(
			`<a href="/"> <button type="button" class="btn btn-elegant btn-lg btn-block container" id="reset">RESET</button></a>`
		);
		$('#resetspot').append($resetBtn);
		$count = 0;

		document.getElementById('reset').addEventListener('click', function(e) {
			//e.preventDefault();
			console.log('reset button clicked');
			get_stats();
		});
	}
}

async function get_stats() {
	const resp = await axios.post('/update-stats', { score: $score });
}
