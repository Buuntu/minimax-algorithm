var app = angular.module("myApp", []);

app.controller('MainController', ['$scope', '$http', function($scope, $http) {
    $scope.inactive = true;
    $scope.loading = false;
    $scope.new_game = true;
    $scope.game_over = false;
    $scope.message = '';
    $scope.winning = [[], [], []];
    $scope.score_player = 0;
    $scope.score_computer = 0;

    $scope.click = function(row, col) {
        // Do nothing if the game is over
        if ($scope.game_over) {
            return;
        }

        if ($scope.board[row][col] === ' ') {
            $scope.board[row][col] = 'X';

            var winning_combo;

            // Player should never win
            if (winning_combo = has_won('X')) {
                for (var i = 0; i < 3; i++) {
                    row = winning_combo[i][0];
                    col = winning_combo[i][1];
                    $scope.winning[row][col] = 1;
                }
                $scope.message = 'You won! :)';
                $scope.score_player++;
                $scope.game_over = true;
                return;
            }
            else if (is_board_full()) {
                $scope.message = 'You tied!';
                $scope.game_over = true;
                return;
            }

            $scope.inactive = true;
            $scope.loading = true;
            $http.post('/move', { player: 'X', computer: 'O', board: $scope.board }).then(function(response) {
                $scope.loading = false;

                if (response.data.hasOwnProperty('computer_row') && response.data.hasOwnProperty('computer_col')) {
                    $scope.board[response.data.computer_row][response.data.computer_col] = 'O'
                }

                if (winning_combo = has_won('O')) {
                    for (var i = 0; i < 3; i++) {
                        row = winning_combo[i][0];
                        col = winning_combo[i][1];
                        $scope.winning[row][col] = 1;
                    }
                    $scope.message = 'You lost :(';
                    $scope.score_computer++;
                    $scope.game_over = true
                }
                else if (is_board_full()) {
                    $scope.message = 'You tied!';
                    $scope.game_over = true;
                }

                $scope.inactive = false;
            }, function(response) {
                $scope.loading = false;
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

    $scope.inactive = false;

    $scope.restart = function() {
        $scope.loading = false;
        $scope.board = angular.copy($scope.blank_board);
        $scope.game_over = false;
        $scope.message = '';
        $scope.winning = [[], [], []];
        $scope.new_game = true;
    };

    $scope.player_goes_first = function() {
        $scope.new_game = false;
    };

    $scope.computer_goes_first = function() {
        $scope.new_game = false;
        $scope.loading = true;

        $http.post('/move', { player: 'X', computer: 'O', board: $scope.board }).then(function(response) {
                $scope.loading = false;

                if (response.data.hasOwnProperty('computer_row') && response.data.hasOwnProperty('computer_col')) {
                    $scope.board[response.data.computer_row][response.data.computer_col] = 'O'
                }

                $scope.inactive = false;
            }, function(response) {
                $scope.loading = false;
                alert('Server error');
            });
    };

    // Returns the winning vertical combination or false
    var has_won = function(mark) {
        var won_horizontal = has_won_horizontal(mark);

        if (won_horizontal) {
            console.log(won_horizontal);
            return won_horizontal;
        }

        var won_vertical = has_won_vertical(mark);

        if (won_vertical) {
            return won_vertical;
        }

        var won_diagonal = has_won_diagonal(mark);

        if (won_diagonal) {
            return won_diagonal;
        }

        return false;
    }

    // Returns the winning combination or false
    var has_won_vertical = function(mark) {
        for (var c = 0; c < 3; c++) {
            if ($scope.board[0][c] == mark && ($scope.board[0][c] == $scope.board[1][c]) && ($scope.board[0][c] == $scope.board[2][c])) {
                return [[0, c], [1, c], [2, c]];
            }
        }

        return false;
    }

    // Returns the winning horizontal combo or false
    var has_won_horizontal = function(mark) {
        for (var r = 0; r < 3; r++) {
            if ($scope.board[r][0] == mark && ($scope.board[r][0] == $scope.board[r][1]) && ($scope.board[r][0] == $scope.board[r][2])) {
                return [[r, 0], [r, 1], [r, 2]];
            }
        }

        return false;
    }

    // Returns the winning diagonal combination or false
    var has_won_diagonal = function(mark) {
        if ($scope.board[0][0] == mark && ($scope.board[0][0] == $scope.board[1][1]) && ($scope.board[0][0] == $scope.board[2][2])) {
            return [[0, 0], [1, 1], [2, 2]];
        }
        else if ($scope.board[2][0] == mark && ($scope.board[2][0] == $scope.board[1][1]) && ($scope.board[2][0] == $scope.board[0][2])) {
            return [[2, 0], [1, 1], [0, 2]];
        }

        return false;
    }

    var is_board_full = function() {
        for (var r = 0; r < 3; r++) {
            for (var c = 0; c < 3; c++) {
                if ($scope.board[r][c] == ' ') {
                    return false;
                }
            }
        }

        return true;
    }

}]);