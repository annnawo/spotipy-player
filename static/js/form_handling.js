
document.addEventListener("DOMContentLoaded", () => {

    // Handle click on star icons
    $('.star-elem').on('click', function () {
        // Reset all stars to unchecked state
        $('.star-elem').removeClass('checked');

        // Mark clicked star and all previous stars as checked
        $(this).addClass('checked');
        $(this).parent().prevAll().find('.star-elem').addClass('checked');
        let rating = $('.star-elem.checked').length;
        update_star_rating(rating);
    });


    let inputRange = document.getElementsByClassName('range')[0],
        maxValue = 100, // the higher the smoother when dragging
        speed = 5,
        currValue, rafID;

    // set min/max value
    inputRange.min = 0;
    inputRange.max = maxValue;

    // set to desired value
    currValue = +this.value;



    // handle range animation
    function animateHandler() {

        // calculate gradient transition
        var transX = currValue - maxValue;

        // update input range
        inputRange.value = currValue;

        //Change slide thumb color on mouse up
        if (currValue < 20) {
            inputRange.classList.remove('ltpurple');
        }
        if (currValue < 40) {
            inputRange.classList.remove('purple');
        }
        if (currValue < 60) {
            inputRange.classList.remove('pink');
        }

        // determine if we need to continue
        if (currValue > -1) {
            window.requestAnimationFrame(animateHandler);
        }

        // decrement value
        currValue = currValue - speed;
    }


    // move gradient
    inputRange.addEventListener('input', function () {
        //Change slide thumb color on way up
        if (this.value > 20) {
            inputRange.classList.add('ltpurple');
        }
        if (this.value > 40) {
            inputRange.classList.add('purple');
        }
        if (this.value > 60) {
            inputRange.classList.add('pink');
        }

        //Change slide thumb color on way down
        if (this.value < 20) {
            inputRange.classList.remove('ltpurple');
        }
        if (this.value < 40) {
            inputRange.classList.remove('purple');
        }
        if (this.value < 60) {
            inputRange.classList.remove('pink');
        }
    });


    // ATMOSPHERE BUTTON DROPDOWN

    const atmosphereBtn = document.querySelector('.atmosphere-btn');
    atmosphereBtn.addEventListener('click', addAtmDropdown);

    function addAtmDropdown() {
        document.getElementById('atmosphere-dropdown-arrow').style.transform = "rotate(180deg)";
        const atmosphereBtnInsert = `
    <div class="atmosphere-dropdown-container">
        <div class="atm-sd">
        <button class="atmosphere-dropdown-option dr-opt" data-atmosphere-option="nostalgic">Nostalgic</button>
        <button class="atmosphere-dropdown-option dr-opt" data-atmosphere-option="hypnotic">Hypnotic</button>
        <button class="atmosphere-dropdown-option dr-opt" data-atmosphere-option="eerie">Eerie</button>
        <button class="atmosphere-dropdown-option dr-opt" data-atmosphere-option="moody">Moody</button>
        <button class="atmosphere-dropdown-option dr-opt" data-atmosphere-option="gritty">Gritty</button>
        <button class="atmosphere-dropdown-option dr-opt" data-atmosphere-option="smooth">Smooth</button>
        <button class="atmosphere-dropdown-option dr-opt" data-atmosphere-option="spirited">Spirited</button>
        <button class="atmosphere-dropdown-option dr-opt" data-atmosphere-option="urban">Urban</button>
        <button class="atmosphere-dropdown-option dr-opt" data-atmosphere-option="verdant">Verdant</button>
        </div><div class="atm-sd">
        <button class="atmosphere-dropdown-option dr-opt" data-atmosphere-option="cinematic">Cinematic</button>
        <button class="atmosphere-dropdown-option dr-opt" data-atmosphere-option="epic">Epic</button>
        <button class="atmosphere-dropdown-option dr-opt" data-atmosphere-option="night">Night</button>
        <button class="atmosphere-dropdown-option dr-opt" data-atmosphere-option="morning">Morning</button>
        <button class="atmosphere-dropdown-option dr-opt" data-atmosphere-option="day">Day</button>
        <button class="atmosphere-dropdown-option dr-opt" data-atmosphere-option="spring">Spring</button>
        <button class="atmosphere-dropdown-option dr-opt" data-atmosphere-option="summer">Summer</button>
        <button class="atmosphere-dropdown-option dr-opt" data-atmosphere-option="fall">Fall</button>
        <button class="atmosphere-dropdown-option dr-opt" data-atmosphere-option="winter">Winter</button>
        </div>
    </div>
    `
        getSelectedAtmospheres();
        const atmosphereDropdownHolder = document.createElement('div');
        atmosphereDropdownHolder.classList.add('atmosphere-dropdown-holder');
        atmosphereDropdownHolder.innerHTML = atmosphereBtnInsert;
        document.querySelector('.atmosphere-btn-div').appendChild(atmosphereDropdownHolder);
        const dropdownOptions = document.querySelectorAll('.atmosphere-dropdown-option');
        dropdownOptions.forEach(option => {
            option.addEventListener('click', function () {
                const atmosphereOption = this.getAttribute('data-atmosphere-option');
                update_atmosphere_option(this, atmosphereOption, 'black');
            })
            option.addEventListener('mouseover', function () {
                option.style.backgroundColor = option.style.borderColor;
                option.style.color = '#ffffff';
            });
            option.addEventListener('mouseout', function () {
                if (!option.classList.contains('included-option')) {
                    option.style.backgroundColor = '';
                    option.style.color = '#000000';
                } else {
                    option.style.backgroundColor = '#000000';
                    option.style.color = '#ffffff';
                }
            });
            option.style.border = 'solid 2px #848DC5';
        });
        atmosphereBtn.removeEventListener('click', addAtmDropdown);
        atmosphereBtn.addEventListener('click', removeAtmDropdown);
    }

    function removeAtmDropdown() {
        const atmosphereDropdownHolder = document.querySelector('.atmosphere-dropdown-holder');
        if (atmosphereDropdownHolder) {
            atmosphereDropdownHolder.remove();
        }
        document.getElementById('atmosphere-dropdown-arrow').style.transform = "rotate(0deg)";
        atmosphereBtn.removeEventListener('click', removeAtmDropdown);
        atmosphereBtn.addEventListener('click', addAtmDropdown);
    }



    // EMOTION BUTTON DROPDOW

    const emotionBtn = document.querySelector('.emotion-btn');
    emotionBtn.addEventListener('click', addEmtDropdown);

    function addEmtDropdown() {
        document.getElementById('emotion-dropdown-arrow').style.transform = "rotate(180deg)";
        const emotionBtnInsert = `
    <div class="emotion-dropdown-container">
        <div class="atm-sd">
        <button class="emotion-dropdown-option dr-opt" data-emotion-option="ecstatic">Ecstatic</button>
        <button class="emotion-dropdown-option dr-opt" data-emotion-option="triumphant">Triumphant</button>
        <button class="emotion-dropdown-option dr-opt" data-emotion-option="hopeful">Hopeful</button>
        <button class="emotion-dropdown-option dr-opt" data-emotion-option="happy">Happy</button>
        <button class="emotion-dropdown-option dr-opt" data-emotion-option="calm">Calm</button>
        <button class="emotion-dropdown-option dr-opt" data-emotion-option="whimsical">Whimsical</button>
        <button class="emotion-dropdown-option dr-opt" data-emotion-option="quirky">Quirky</button>
        <button class="emotion-dropdown-option dr-opt" data-emotion-option="comical">Comical</button>
        </div><div class="atm-sd">
        <button class="emotion-dropdown-option dr-opt" data-emotion-option="inspired">Inspired</button>
        <button class="emotion-dropdown-option dr-opt" data-emotion-option="cathartic">Cathartic</button>
        <button class="emotion-dropdown-option dr-opt" data-emotion-option="frenetic">Frenetic</button>
        <button class="emotion-dropdown-option dr-opt" data-emotion-option="anxious">Anxious</button>
        <button class="emotion-dropdown-option dr-opt" data-emotion-option="angry">Angry</button>
        <button class="emotion-dropdown-option dr-opt" data-emotion-option="envious">Envious</button>
        <button class="emotion-dropdown-option dr-opt" data-emotion-option="melancholic">Melancholic</button>
        <button class="emotion-dropdown-option dr-opt" data-emotion-option="wistful">Wistful</button>
        </div>
    </div>
    `
        getSelectedEmotions();
        const emotionDropdownHolder = document.createElement('div');
        emotionDropdownHolder.classList.add('emotion-dropdown-holder');
        emotionDropdownHolder.innerHTML = emotionBtnInsert;
        document.querySelector('.emotion-btn-div').appendChild(emotionDropdownHolder);
        const dropdownOptions = document.querySelectorAll('.emotion-dropdown-option');
        dropdownOptions.forEach(option => {
            option.addEventListener('click', function () {
                const emotionOption = this.getAttribute('data-emotion-option');
                update_emotion_option(this, emotionOption, 'black');
            })
            option.addEventListener('mouseover', function () {
                option.style.backgroundColor = option.style.borderColor;
                option.style.color = '#ffffff';
            });
            option.addEventListener('mouseout', function () {
                if (!option.classList.contains('included-option')) {
                    option.style.backgroundColor = '';
                    option.style.color = '#000000';
                } else {
                    option.style.backgroundColor = '#000000';
                    option.style.color = '#ffffff';
                }
            });
            option.style.border = 'solid 2px #848DC5';
        });
        emotionBtn.removeEventListener('click', addEmtDropdown);
        emotionBtn.addEventListener('click', removeEmtDropdown);
    }

    function removeEmtDropdown() {
        const emotionDropdownHolder = document.querySelector('.emotion-dropdown-holder');
        if (emotionDropdownHolder) {
            emotionDropdownHolder.remove();
        }
        document.getElementById('emotion-dropdown-arrow').style.transform = "rotate(0deg)";
        emotionBtn.removeEventListener('click', removeEmtDropdown);
        emotionBtn.addEventListener('click', addEmtDropdown);
    }


    // TAG BUTTON DROPDOWN
    const tagBtn = document.querySelector('.tag-btn');
    tagBtn.addEventListener('click', addTagDropdown);
    function addTagDropdown() {
        document.getElementById('tag-dropdown-arrow').style.transform = "rotate(180deg)";

        let tagInsert = `
        <form id="tag-form">
        <input type="text" id="tag-input-field">
        <button type="submit" id="add-tag" class="tag-dropdown-option dr-opt">Add Tag</button>
        </form>
        <hr class="tag-form-hr">
        <div class="tag-dropdown-container">  
        </div>
        `
        const tagDropdownHolder = document.createElement('div');
        tagDropdownHolder.classList.add('tag-dropdown-holder');
        tagDropdownHolder.innerHTML = tagInsert;
        const tagInputField = tagDropdownHolder.querySelector('#tag-input-field');
        document.querySelector('.tag-btn-div').appendChild(tagDropdownHolder);
        document.querySelector('#tag-form').addEventListener('submit', (event) => {
            event.preventDefault();
            let tagToAdd = tagInputField.value;
            if (tagToAdd !== null && tagToAdd.trim() !== '') {
                console.log('here!!!')
                tagInputField.value = '';
                add_tag_option(tagToAdd);
            }
        })
        getAllTags();
        tagBtn.removeEventListener('click', addTagDropdown);
        tagBtn.addEventListener('click', removeTagDropdown);
    }

    function removeTagDropdown() {
        const tagDropdownHolder = document.querySelector('.tag-dropdown-holder');
        if (tagDropdownHolder) {
            tagDropdownHolder.remove();
        }
        document.getElementById('tag-dropdown-arrow').style.transform = "rotate(0deg)";
        tagBtn.removeEventListener('click', removeTagDropdown);
        tagBtn.addEventListener('click', addTagDropdown);
    }


    // ENERGY SLIDER
    const energySlider = document.querySelector('.energy-slider');
    energySlider.addEventListener('change', () => {
        let value = energySlider.value;
        add_song_energy_level(value);
    });

    // PAUSE AND PLAY PSEUDO-BUTTONS
    let pauseBtn = document.querySelector('.pause-icon');
    if (pauseBtn == null) {
        let playBtn = document.querySelector('.play-icon');
        playBtn.addEventListener('click', resumePlayback);
    } else {
        pauseBtn.addEventListener('click', pausePlayback);
    }


    function pausePlayback() {
        fetch('/pause_playback/', {
            method: 'GET',
        })
            .then(response => {
                if (response.ok) {
                    playBtn = document.createElement('div');
                    playBtn.classList.add('play-icon');
                    playBtn.innerHTML = `<img src='../static/images/play_icon.png' alt="Play song icon">`;
                    pauseBtn.removeEventListener('click', pausePlayback);
                    pauseBtn.parentNode.replaceChild(playBtn, pauseBtn);
                    playBtn.addEventListener('click', resumePlayback);
                } else {
                    // Handle errors if any
                    console.error('Error pausing');
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }

    function resumePlayback() {
        fetch('/resume_playback/', {
            method: 'GET',
        })
            .then(response => {
                if (response.ok) {
                    pauseBtn = document.createElement('div');
                    pauseBtn.classList.add('pause-icon');
                    pauseBtn.innerHTML = `<img src='../static/images/pause_icon.png' alt="Pause song icon">`;
                    playBtn.removeEventListener('click', resumePlayback);
                    playBtn.parentNode.replaceChild(pauseBtn, playBtn);
                    pauseBtn.addEventListener('click', pausePlayback);
                } else {
                    // Handle errors if any
                    console.error('Error pausing');
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }


    // OTHER MUSIC CONTROLS (SKIP, GO BACK)
    let skipBtn = document.querySelector('.skip-icon');
    let previousBtn = document.querySelector('.previous-song-icon');
    skipBtn.addEventListener('click', () => {
        const songDetailsElement = document.querySelector('.pbmc-song-details');
        let trackId = songDetailsElement.getAttribute('data-track-id');
        $.ajax({
            url: '/skip_song/' + trackId,
            type: 'GET',
            success: function (response) {
                window.location.href = '/player/';
            },
            error: function (xhr, status, error) {
                console.error('Error checking library:', error);
            }
        });
    })
    previousBtn.addEventListener('click', () => {
        fetch('/play_previous_song/', {
            method: 'GET',
        })
            .then(response => {
                if (response.ok) {
                    window.location.href = '/player/';

                } else {
                    // Handle errors if any
                    console.error('Error skipping');
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    })


    // function getAllTags() {
    //     let tagDropdownContainer = document.querySelector('.tag-dropdown-container');
    //     let tagBtnDiv1 = document.createElement('div');
    //     let tagBtnDiv2 = document.createElement('div');
    //     tagBtnDiv1.classList.add('atm-sd');
    //     tagBtnDiv2.classList.add('atm-sd');
    //     let selectedTags = getSelectedTags();
    //     console.log(selectedTags);
    //     let myArray = ["Americana"];
    //     console.log(myArray);
    //     $.ajax({
    //         url: '/get_all_user_tags/',
    //         type: 'GET',
    //         success: function (response) {
    //             if (response.tags) {
    //                 let counter = 0;
    //                 response.tags.forEach(function (tag) {
    //                     let tagOptionBtn = document.createElement('button');
    //                     tagOptionBtn.classList.add('tag-dropdown-option', 'dr-opt');
    //                     tagOptionBtn.setAttribute('data-tag-option', tag);
    //                     tagOptionBtn.textContent = tag; // Set the text content of the button
                        
    //                     tagOptionBtn.addEventListener('mouseover', function () {
    //                         tagOptionBtn.style.backgroundColor = tagOptionBtn.style.borderColor;
    //                         tagOptionBtn.style.color = '#ffffff';
    //                     });
                        
    //                     tagOptionBtn.addEventListener('mouseout', function () {
    //                         if (!tagOptionBtn.classList.contains('included-option')) {
    //                             tagOptionBtn.style.backgroundColor = '';
    //                             tagOptionBtn.style.color = '#000000';
    //                         } else {
    //                             tagOptionBtn.style.backgroundColor = '#000000';
    //                             tagOptionBtn.style.color = '#ffffff';
    //                         }
    //                     });
    //                     console.log('right before execution');
    //                     if (selectedTags.includes("Americana")) {
    //                         console.log('CONTAINSSSSSS');
    //                     //     tagOptionBtn.classList.add('included-option');
    //                     //     tagOptionBtn.style.backgroundColor = '#000000';
    //                     //     tagOptionBtn.style.color = '#ffffff';
    //                     }
    //                     if (myArray.includes("Americana")) {
    //                         console.log("what the fuck is going on here");
    //                     }
                        
    //                     if ((counter % 2) == 0) {
    //                         tagBtnDiv1.appendChild(tagOptionBtn);
    //                     } else {
    //                         tagBtnDiv2.appendChild(tagOptionBtn);
    //                     }
    //                     // let tagOptionBtn = `<button class="tag-dropdown-option dr-opt" data-tag-option="${tag}">${tag}</button>`
    //                     // console.log(tag);
    //                 });
    //                 tagDropdownContainer.appendChild(tagBtnDiv1);
    //                 tagDropdownContainer.appendChild(tagBtnDiv2);

    //             }
    //         },
    //         error: function (xhr, status, error) {
    //             console.error('Error checking library:', error);
    //         }
    //     });


    // }

});


//////

function getSelectedAtmospheres() {
    const songDetailsElement = document.querySelector('.pbmc-song-details');
    let trackId = songDetailsElement.getAttribute('data-track-id');
    $.ajax({
        url: '/get_atmospheres/' + trackId,
        type: 'GET',
        success: function (response) {
            if (response.atmospheres) {
                response.atmospheres.forEach(function (atmosphere) {
                    let atmosphereOptionBtn = document.querySelector(`.atmosphere-dropdown-option[data-atmosphere-option="${atmosphere}"]`);
                    atmosphereOptionBtn.classList.add('included-option');
                    atmosphereOptionBtn.style.backgroundColor = '#000000';
                    atmosphereOptionBtn.style.color = '#ffffff';
                });
            }

        },
        error: function (xhr, status, error) {
            console.error('Error checking library:', error);
        }
    });
}


function getSelectedEmotions() {
    const songDetailsElement = document.querySelector('.pbmc-song-details');
    let trackId = songDetailsElement.getAttribute('data-track-id');
    $.ajax({
        url: '/get_emotions/' + trackId,
        type: 'GET',
        success: function (response) {
            if (response.emotions) {
                response.emotions.forEach(function (emotion) {
                    let emotionOptionBtn = document.querySelector(`.emotion-dropdown-option[data-emotion-option="${emotion}"]`);
                    emotionOptionBtn.classList.add('included-option');
                    emotionOptionBtn.style.backgroundColor = '#000000';
                    emotionOptionBtn.style.color = '#ffffff';
                });
            }

        },
        error: function (xhr, status, error) {
            console.error('Error checking library:', error);
        }
    });
}


function getAllTags() {
    let tagDropdownContainer = document.querySelector('.tag-dropdown-container');
    let tagBtnDiv1 = document.createElement('div');
    let tagBtnDiv2 = document.createElement('div');
    tagBtnDiv1.classList.add('atm-sd');
    tagBtnDiv2.classList.add('atm-sd');
    
    // Call getSelectedTags with getAllTags as its callback function
    getSelectedTags(function(selectedTags) {
        console.log(selectedTags);
        
        // Proceed with the rest of the code only after getSelectedTags is done
        $.ajax({
            url: '/get_all_user_tags/',
            type: 'GET',
            success: function (response) {
                if (response.tags) {
                    let counter = 0;
                    response.tags.forEach(function (tag) {
                        let tagOptionBtn = document.createElement('button');
                        tagOptionBtn.classList.add('tag-dropdown-option', 'dr-opt');
                        tagOptionBtn.setAttribute('data-tag-option', tag);
                        tagOptionBtn.textContent = tag;
                        tagOptionBtn.style.border = 'solid 2px #848DC5';

                        if (selectedTags.includes(tag)) {
                            tagOptionBtn.classList.add('included-option');
                            tagOptionBtn.style.backgroundColor = '#000000';
                            tagOptionBtn.style.color = '#ffffff';
                        }

                        tagOptionBtn.addEventListener('click', function () {
                            const tagOption = this.getAttribute('data-tag-option');
                            update_tag_option(this, tagOption, 'black');
                        })

                        tagOptionBtn.addEventListener('mouseover', function () {
                            tagOptionBtn.style.backgroundColor = tagOptionBtn.style.borderColor;
                            tagOptionBtn.style.color = '#ffffff';
                        });
                        
                        tagOptionBtn.addEventListener('mouseout', function () {
                            if (!tagOptionBtn.classList.contains('included-option')) {
                                tagOptionBtn.style.backgroundColor = '';
                                tagOptionBtn.style.color = '#000000';
                            } else {
                                tagOptionBtn.style.backgroundColor = '#000000';
                                tagOptionBtn.style.color = '#ffffff';
                            }
                        });
                        
                        // Append the button to the correct div
                        if ((counter % 2) == 0) {
                            tagBtnDiv1.appendChild(tagOptionBtn);
                            counter++;
                        } else {
                            tagBtnDiv2.appendChild(tagOptionBtn);
                            counter++;
                        }
                    });

                    // Append the divs to the container
                    tagDropdownContainer.appendChild(tagBtnDiv1);
                    tagDropdownContainer.appendChild(tagBtnDiv2);
                }
            },
            error: function (xhr, status, error) {
                console.error('Error checking library:', error);
            }
        });
    });
}

function getSelectedTags(callback) {
    const songDetailsElement = document.querySelector('.pbmc-song-details');
    let trackId = songDetailsElement.getAttribute('data-track-id');
    let selectedTags = [];
    $.ajax({
        url: '/get_tags/' + trackId,
        type: 'GET',
        success: function (response) {
            if (response.tags) {
                response.tags.forEach(function (tag) {
                    selectedTags.push(tag);
                });
            }
            callback(selectedTags); // Call the callback function with the retrieved data
        },
        error: function (xhr, status, error) {
            console.error('Error checking library:', error);
            callback([]); // Call the callback function with an empty array in case of error
        }
    });
}



// function getSelectedTags() {
//     const songDetailsElement = document.querySelector('.pbmc-song-details');
//     let trackId = songDetailsElement.getAttribute('data-track-id');
//     let selectedTags = [];
//     $.ajax({
//         url: '/get_tags/' + trackId,
//         type: 'GET',
//         success: function (response) {
//             if (response.tags) {
//                 response.tags.forEach(function (tag) {
//                     selectedTags.push(tag);
//                 });
//             }
//         },
//         error: function (xhr, status, error) {
//             console.error('Error checking library:', error);
//         }
//     });
//     return selectedTags;
// }

//

function checkLibrary(spotifyId) {
    $.ajax({
        url: '/check_library/' + spotifyId,
        type: 'GET',
        success: function (response) {
            if (response.in_library) {
                // Song is in library, update UI accordingly (e.g., change button text)
                $('.add-to-library-btn').text('Remove from Library');
            } else {
                // Song is not in library
                $('.add-to-library-btn').text('Add to Library');
            }
        },
        error: function (xhr, status, error) {
            console.error('Error checking library:', error);
        }
    });
}


function checkListenAgain(spotifyId) {
    $.ajax({
        url: '/check_listen_again/' + spotifyId,
        type: 'GET',
        success: function (response) {
            if (response.in_listen_again) {
                // Song is in library, update UI accordingly (e.g., change button text)
                $('.listen-again-btn').text('Remove from Listen Again');
            } else {
                // Song is not in library
                $('.listen-again-btn').text('Listen Again');
            }
        },
        error: function (xhr, status, error) {
            console.error('Error checking library:', error);
        }
    });
}


function updateCheckedStars(spotifyId) {
    $.ajax({
        url: '/get_rating/' + spotifyId,
        type: 'GET',
        success: function (response) {
            if (response.star_ct) {
                var stars = $('.star-elem');
                stars.removeClass('checked'); // Remove current checks

                if (response.star_ct) {
                    // If there is a rating, check the stars up to that count
                    stars.each(function () {
                        var star = $(this);
                        if (star.data('rating') <= response.star_ct) {
                            star.addClass('checked');
                        }
                    });
                }
            }
        },
        error: function (xhr, status, error) {
            console.error('Error checking library:', error);
        }
    });
}


let playlistSongMgmtBtn = document.querySelector('.playlist-form-block-btn-player');
playlistSongMgmtBtn.addEventListener('click', playlistQuickMgmt);
function playlistQuickMgmt() {
    const songDetailsElement = document.querySelector('.pbmc-song-details');
    let trackId = songDetailsElement.getAttribute('data-track-id');
    let quickAddInsert = ` <div class="quick-add-container"> </div> `;
    let quickAddElem = document.createElement('div');
    quickAddElem.classList.add('quick-add-holder');
    quickAddElem.innerHTML = quickAddInsert;
    let playlistBlockDiv = document.querySelector('.playlists-append');
    playlistBlockDiv.prepend(quickAddElem);
    qaAppend = document.querySelector('.quick-add-container');
    // let selectedTags = [];
    $.ajax({
        url: '/get_quick_select_playlists/' + trackId,
        type: 'GET',
        success: function (response) {
            var playlists = JSON.parse(response);

            // Iterate over each playlist
            playlists.forEach(function (playlist) {
                let playlistOptionInsert = document.createElement('div');
                playlistOptionInsert.classList.add('playlist-option')
                if (playlist.track_in_playlist) {
                    playlistOptionInsert.innerHTML = `

                        <div data-playlist-id="${playlist.id}">${playlist.name}</div>
                        <button class="playlist-option-button-qa"><span class="faboxes"><i class="fa fa-check-square-o"></span></i></button>

                    `
                } else {
                    playlistOptionInsert.innerHTML = `

                        <div data-playlist-id="${playlist.id}">${playlist.name}</div>
                        <button class="playlist-option-button-qa"><span class="faboxes"><i class="fa fa-square-o"></span></i></button>

                    `
                }
                qaAppend.appendChild(playlistOptionInsert);
            });
        
        },
        error: function (xhr, status, error) {
            console.error('Error checking library:', error);
        }
    });
}