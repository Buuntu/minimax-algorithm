var app = angular.module("myApp", []);

app.controller('MainController', ['$scope', '$http', function($scope, $http) {
    $scope.inactive = true;

    $scope.click = function(row, col) {
        if ($scope.board[row][col] === ' ') {
            $scope.board[row][col] = 'X';
            $scope.inactive = true;
            $http.post('/move', { player: 'X', computer: 'O', board: $scope.board }).then(function(response) {
                console.log(response);
                console.log(response.data.player_wins);
                if (response.data.player_wins) {
                    alert('Player won!');
                }
                else if (response.data.computer_wins) {
                    alert('Computer won!');
                }

                if (response.data.hasOwnProperty('computer_row') && response.data.hasOwnProperty('computer_col')) {
                    $scope.board[response.data.computer_row][response.data.computer_col] = 'O'
                }

                $scope.inactive = false;
            }, function(response) {
                alert('Server error');
            });
        }
    };

    $scope.blank_board = [
        [' ', ' ', ' '],
        [' ', ' ', ' '],
        [' ', ' ', ' ']
    ];

    $scope.board = angular.copy($scope.blank_board);

    var turn = {
        'computer': 0,
        'human': 1
    };

    $scope.turn = turn['computer'];

    $scope.inactive = false;

    $scope.restart = function() {
        $scope.board = angular.copy($scope.blank_board);
    };
}]);