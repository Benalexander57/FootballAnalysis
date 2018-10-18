class Competition(object):
    # The class "constructor" - It's actually an initializer 
    def __init__(self, competitionId, seasonId, countryName, competitionName, seasonName, matchUpdatedDttm, matchAvailableDttm):
        self.competitionId = competitionId
        self.seasonId = seasonId        
        self.countryName = countryName
        self.competitionName = competitionName
        self.seasonName = seasonName
        self.matchUpdatedDttm = matchUpdatedDttm
        self.matchAvailableDttm = matchAvailableDttm

def create_competition(competitionId, seasonId, countryName, competitionName, seasonName, matchUpdatedDttm, matchAvailableDttm):
    competition = Competition(competitionId, seasonId, countryName, competitionName, seasonName, matchUpdatedDttm, matchAvailableDttm)
    return competition