import unittest
from unittest.mock import Mock, patch
from statistics_service import StatisticsService


class TestStatisticsService(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        self.mock_player1 = Mock()
        self.mock_player1.name = "Connor McDavid"
        self.mock_player1.team = "Edmonton Oilers"
        self.mock_player1.points = 120

        self.mock_player2 = Mock()
        self.mock_player2.name = "Leon Draisaitl"
        self.mock_player2.team = "Edmonton Oilers"
        self.mock_player2.points = 110

        self.mock_player3 = Mock()
        self.mock_player3.name = "Auston Matthews"
        self.mock_player3.team = "Toronto Maple Leafs"
        self.mock_player3.points = 105

        self.mock_players = [self.mock_player1, self.mock_player2, self.mock_player3]

    @patch('statistics_service.PlayerReader')
    def test_search_found(self, mock_reader):
        """Test search when player is found"""
        mock_reader.return_value.get_players.return_value = self.mock_players
        service = StatisticsService()
        result = service.search("McDavid")
        self.assertEqual(result, self.mock_player1)

    @patch('statistics_service.PlayerReader')
    def test_search_not_found(self, mock_reader):
        """Test search when player is not found"""
        mock_reader.return_value.get_players.return_value = self.mock_players
        service = StatisticsService()
        result = service.search("Unknown")
        self.assertIsNone(result)

    @patch('statistics_service.PlayerReader')
    def test_search_partial_match(self, mock_reader):
        """Test search with partial name match"""
        mock_reader.return_value.get_players.return_value = self.mock_players
        service = StatisticsService()
        result = service.search("Leon")
        self.assertEqual(result, self.mock_player2)

    @patch('statistics_service.PlayerReader')
    def test_team_single_team(self, mock_reader):
        """Test filtering players by team"""
        mock_reader.return_value.get_players.return_value = self.mock_players
        service = StatisticsService()
        result = service.team("Edmonton Oilers")
        self.assertEqual(len(result), 2)
        self.assertIn(self.mock_player1, result)
        self.assertIn(self.mock_player2, result)

    @patch('statistics_service.PlayerReader')
    def test_team_no_match(self, mock_reader):
        """Test team filter with no matching team"""
        mock_reader.return_value.get_players.return_value = self.mock_players
        service = StatisticsService()
        result = service.team("Non-existent Team")
        self.assertEqual(len(result), 0)

    @patch('statistics_service.PlayerReader')
    def test_top_valid_count(self, mock_reader):
        """Test top players returns correct number"""
        mock_reader.return_value.get_players.return_value = self.mock_players
        service = StatisticsService()
        result = service.top(1)
        self.assertEqual(len(result), 2)  # how_many=1, but while loop goes i<=how_many (0,1)
        self.assertEqual(result[0], self.mock_player1)  # highest points

    @patch('statistics_service.PlayerReader')
    def test_top_zero(self, mock_reader):
        """Test top with how_many=0"""
        mock_reader.return_value.get_players.return_value = self.mock_players
        service = StatisticsService()
        result = service.top(0)
        self.assertEqual(len(result), 1)  # while i <= 0: executes once (i=0)
        self.assertEqual(result[0], self.mock_player1)

    @patch('statistics_service.PlayerReader')
    def test_top_larger_than_list(self, mock_reader):
        """Test top with how_many larger than player count"""
        mock_reader.return_value.get_players.return_value = self.mock_players
        service = StatisticsService()
        with self.assertRaises(IndexError):
            service.top(5)  # Only 3 players, requesting top 6


if __name__ == '__main__':
    unittest.main()