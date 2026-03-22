# File: models.py
# Author: Nicholas Sima (nicksima@bu.edu)
# Description: models file to hold Voter class definition and CSV data loader

from django.db import models
import csv
import os

# Create your models here.

class Voter(models.Model):
    '''Encapsulate a registered voter from Newton, MA'''

    # identity
    last_name = models.TextField()
    first_name = models.TextField()

    # address
    street_number = models.TextField()
    street_name = models.TextField()
    apt = models.TextField(blank=True)
    zip_code = models.TextField()

    # registration info
    dob = models.DateField()
    date_registered = models.DateField()
    party = models.CharField(max_length=5)
    precinct = models.CharField(max_length=10)

    # election participation
    v20state = models.BooleanField(default=False)
    v21town = models.BooleanField(default=False)
    v21primary = models.BooleanField(default=False)
    v22general = models.BooleanField(default=False)
    v23town = models.BooleanField(default=False)
    voter_score = models.IntegerField(default=0)

    def __str__(self):
        '''Return a string representation of the voter.'''

        return f'{self.first_name} {self.last_name}, {self.party.strip()}, score={self.voter_score}'


def load_data():
    '''Load voter records from the Newton CSV file into the database.'''

    # CSV path, also pushed to git for modularity :D
    csv_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'media', 'voter_analytics', 'newton_voters.csv'
    )

    # empty records before loading
    Voter.objects.all().delete()

    count = 0
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            try:
                Voter.objects.create(
                    last_name=row['Last Name'],
                    first_name=row['First Name'],
                    street_number=row['Residential Address - Street Number'],
                    street_name=row['Residential Address - Street Name'],
                    apt=row['Residential Address - Apartment Number'],
                    zip_code=row['Residential Address - Zip Code'],
                    dob=row['Date of Birth'],
                    date_registered=row['Date of Registration'],
                    party=row['Party Affiliation'],
                    precinct=row['Precinct Number'],
                    v20state=row['v20state'] == 'TRUE',
                    v21town=row['v21town'] == 'TRUE',
                    v21primary=row['v21primary'] == 'TRUE',
                    v22general=row['v22general'] == 'TRUE',
                    v23town=row['v23town'] == 'TRUE',
                    voter_score=int(row['voter_score']),
                )
                count += 1
            except Exception as e:
                # skip bad data
                print(f'Skipping row due to error: {e}')

    print(f'Done. Loaded {count} voters.')
