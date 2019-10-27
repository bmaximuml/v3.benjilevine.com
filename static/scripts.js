document.addEventListener('click', function(e) {
    let clicked = getTarget(e, 'UL', 'A', 'SPAN');
    if (clicked.tagName !== 'LI') {
        return;
    }
    let content = document.getElementById(clicked.id + '-content');
    let tabs = document.getElementById('projects-tabs');
    let projects_content = document.getElementById('projects-content');

    for (const child of tabs.children) {
        child.classList.remove('is-active');
    }
    clicked.classList.add('is-active');

    for (const child of projects_content.children) {
        child.classList.add('is-hidden');
    }
    content.classList.remove('is-hidden');
});

function getTarget(e, parent = '', child = '', grandchild = '') {
    e = e || Event;
    let target = e.target || Event.target;

    if (target.tagName === parent) {
        target = target.firstElementChild;
    }
    else if (target.tagName === child) {
        target = target.parentElement;
    }
    else if (target.tagName === grandchild) {
        target = target.parentElement.parentElement;
    }

    return target;
}
