const app = angular.module("myApp", []);

app.config(function ($interpolateProvider) {
    $interpolateProvider.startSymbol('{[{');
    $interpolateProvider.endSymbol('}]}');
});

app.config(['$httpProvider', function ($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

app.controller("navbarCtrl", function ($scope, $http, $window) {
    $scope.username = global.username;
    $scope.isAuthenticated = global.isAuthenticated;
    $scope.isSuperuser = global.isSuperuser;
});

app.controller("loginCtrl", function ($scope, $http, $window) {
    $scope.data = {};
    $scope.error = '';

    $scope.submit = function () {
        $scope.error = '';
        $http({
            method: 'POST',
            url: '/accounts/login',
            data: $scope.data
        }).then(function successCallback(response) {
            $window.location.href = '/'; // redirect to home page
        }, function errorCallback(response) {
            $scope.error = response.data.message
        });
    }
});

app.controller("registerCtrl", function ($scope, $http, $window) {
    $scope.data = {};
    $scope.error = '';

    $scope.submit = function () {
        $scope.error = '';
        $http({
            method: 'POST',
            url: '/accounts/register',
            data: $scope.data
        }).then(function successCallback(response) {
            $window.location.href = '/'; // redirect to home page
        }, function errorCallback(response) {
            $scope.error = response.data.message
        });
    }
});

app.controller("managementCtrl", function ($scope, $http, $window) {
    $scope.users = [];
    $scope.error = "";
    $scope.amountUsers = 0;
    $scope.amountPosts = 0;
    $scope.amountReviews = 0;

    $scope.getUsers = function () {
        $http({
            method: 'GET',
            url: '/accounts/get_users',
        }).then(function successCallback(response) {
            $scope.users = response.data.users
        }, function errorCallback(response) {
            $scope.error = response.data.message
        });
    }
    $scope.getReview = function () {
        $http({
            method: 'GET',
            url: '/get_reviews',
        }).then(function successCallback(response) {
            $scope.reviews = response.data.reviews
        }, function errorCallback(response) {
            $scope.error = response.data.message
        });
    }
    $scope.deleteUser = function (userId) {
        $http({
            method: 'DELETE',
            url: '/accounts/delete_user',
            params: {
                user_id: userId
            }
        }).then(function successCallback(response) {
            $scope.getUsers();
        }, function errorCallback(response) {
            $scope.error = response.data.message
        });
    }
    $scope.getStats = function () {
        $http({
            method: 'GET',
            url: '/get_stats',
        }).then(function successCallback(response) {
            $scope.amountUsers = response.data.amount_users;
            $scope.amountPosts = response.data.amount_posts;
            $scope.amountReviews = response.data.amount_reviews;
        }, function errorCallback(response) {
            $scope.error = response.data.message
        });
    }

    $scope.getUsers();
    $scope.getReview();
    $scope.getStats();
});


app.controller("homeCtrl", function ($scope, $http) {
    $scope.isAuthenticated = global.isAuthenticated;
    $scope.username = global.username;
    $scope.categories = [];
    $scope.status = [];
    $scope.postData = {};
    $scope.reviewData = {};
    $scope.uploadedImage = undefined;
    $scope.error = '';
    $scope.posts = [];
    $scope.currentCategory = '';
    $scope.showMyPosts = false;
    $scope.showFavorites = false;
    $scope.postToEdit = {};
    $scope.passwordToEdit = {};
    $scope.profileToEdit = {};
    $scope.postToShowContacts = {};
    $scope.isSuperuser = global.isSuperuser;
    $scope.search = '';

    $scope.addToFavorite = function (post_id) {
        $http({
            method: 'POST',
            url: '/add_to_favorite',
            data: {
                post_id: post_id
            }
        }).then(function successCallback(response) {
            $scope.getPosts();
        }, function errorCallback(response) {
            $scope.error = response.data.message
        });
    }

    //Get the button
    let mybutton = document.getElementById("btn-back-to-top");

    // When the user scrolls down 20px from the top of the document, show the button
    window.onscroll = function () {
        scrollFunction();
    };

    function scrollFunction() {
        if (
            document.body.scrollTop > 20 ||
            document.documentElement.scrollTop > 20
        ) {
            mybutton.style.display = "block";
        } else {
            mybutton.style.display = "none";
        }
    }

    // When the user clicks on the button, scroll to the top of the document
    mybutton.addEventListener("click", backToTop);

    function backToTop() {
        document.body.scrollTop = 0;
        document.documentElement.scrollTop = 0;
    }

    $scope.toggleShowMyPosts = function () {
        $scope.showMyPosts = !$scope.showMyPosts;
        $scope.getPosts();
    }
    $scope.toggleShowFavorites = function () {
        $scope.showFavorites = !$scope.showFavorites;
        $scope.getPosts();
    }
    $scope.setCurrentCategory = function (category) {
        if ($scope.currentCategory === category) {
            $scope.currentCategory = '';
        } else {
            $scope.currentCategory = category;
        }
        $scope.getPosts();
    }
    $scope.getCategories = function () {
        $http({
            method: 'GET',
            url: '/get_categories',
        }).then(function successCallback(response) {
            $scope.categories = response.data.categories
        }, function errorCallback(response) {
            $scope.error = response.data.message
        });
    }
    $scope.getStatus = function () {
        $http({
            method: 'GET',
            url: '/get_status',
        }).then(function successCallback(response) {
            $scope.status = response.data.status
        }, function errorCallback(response) {
            $scope.error = response.data.message
        });
    }

    $scope.getPosts = function () {
        let params = {}
        if ($scope.currentCategory) {
            params['category'] = $scope.currentCategory
        }
        if ($scope.showMyPosts) {
            params['author__id'] = global.userId
        }
        if ($scope.showFavorites) {
            params['is_favorite'] = true
        }
        $http({
            method: 'GET',
            url: '/get_posts',
            params: params
        }).then(function successCallback(response) {
            $scope.posts = response.data.posts
        }, function errorCallback(response) {
            $scope.error = response.data.message
        });
    }
    $scope.onSelectFile = function ($files) {
        for (var i = 0; i < $files.length; i++) {
            var $file = $files[i];
            debugger;
            $upload.upload({
                url: 'api/HomeControler/upload',
                file: $file,
                progress: function (e) {
                    // wait...
                }
            })
                .then(function (data, status, headers, config) {
                    alert('file is uploaded successfully');
                });
        }
        alert('file is uploaded successfully');
    }
    $scope.createPost = function () {
        var fd = new FormData();
        fd.append('data', angular.toJson($scope.postData));
        if ($scope.file) {
            fd.append("file", $scope.file, $scope.file.name);
        }
        return $http.post('create_post', fd, {
            transformRequest: angular.identity,
            headers: {
                'Content-Type': undefined
            }
        }).then(function successCallback(response) {
            console.log(response)
            $('#addPostModal').modal('hide');
            $scope.postData = {};
            $scope.getPosts();
        }, function errorCallback(response) {
            $scope.error = response.data.message
        });
    }
    $scope.createReview = function () {
        $scope.error = '';
        $http({
            method: 'POST',
            url: '/create_review',
            data: $scope.reviewData
        }).then(function successCallback(response) {
            console.log(response)
            $('#addReviewModal').modal('hide');
            $scope.reviewData = {};
            $scope.getReview();
        }, function errorCallback(response) {
            $scope.error = response.data.message
        });
    }

    $scope.edit = function (post) {
        $scope.postToEdit = {...post};
        $scope.postToEdit['category'] = post['category__title']
    }
    $scope.showContacts = function (post) {
        $scope.postToShowContacts = {...post};
    }
    $scope.editPost = function () {
        var fd = new FormData();
        fd.append('data', angular.toJson($scope.postToEdit));
        if ($scope.file) {
            fd.append("file", $scope.file, $scope.file.name);
        }

        return $http.post('edit_post/' + $scope.postToEdit.id, fd, {
            transformRequest: angular.identity,
            headers: {
                'Content-Type': undefined
            }
        }).then(function successCallback(response) {
            $('#editPostModal').modal('hide');
            $scope.postToEdit = {};
            $scope.getPosts();
        }, function errorCallback(response) {
            $scope.error = response.data.message
        });
    }

    $scope.deletePosts = function (post_id) {
        $http({
            method: 'DELETE',
            url: '/delete_post/' + post_id,
        }).then(function successCallback(response) {
            $scope.getPosts();
        }, function errorCallback(response) {
            $scope.error = response.data.message
        });
    }

    $scope.editProfile = function () {
        $http({
            method: 'POST',
            url: '/edit_profile',
            data: $scope.profileToEdit
        }).then(function successCallback(response) {
            $('#editProfileModal').modal('hide');
            $scope.profileToEdit = {};
            location.reload();
        }, function errorCallback(response) {
            $scope.error = response.data.message
        });
    }
    $scope.changePassword = function () {
            $http({
            method: 'POST',
            url: '/change_password',
            data: $scope.passwordToEdit
        }).then(function successCallback(response) {
            $('#changePasswordModal').modal('hide');
            $scope.passwordToEdit = {};
            location.reload();
        }, function errorCallback(response) {
            $scope.error = response.data.message
        });
    }

    $scope.getCategories();
    $scope.getPosts();
    $scope.getStatus();
});


app.directive('file', function () {
    return {
        scope: {
            file: '='
        },
        link: function (scope, el, attrs) {
            el.bind('change', function (event) {
                var file = event.target.files[0];
                scope.file = file ? file : undefined;
                scope.$apply();
            });
        }
    };
});

 
