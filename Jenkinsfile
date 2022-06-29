pipeline {
    agent any
//    environment {
//        GITHUB_AUTH_TOKEN = ''
//        }
    stages {
        stage('Score-nixpkgs-NixOS') {
            steps {
                sh '/usr/bin/scorecard-linux-amd64 --repo=https://github.com/NixOS/nixpkgs'
            }
        }
        stage('Score-tiiuae-spectrum') {
            steps {
                sh '/usr/bin/scorecard-linux-amd64 --repo=https://github.com/tiiuae/spectrum'
            }
        }
        stage('Score-tiiuae-nixpkgs-spectrum') {
            steps {
                sh '/usr/bin/scorecard-linux-amd64 --repo=https://github.com/tiiuae/nixpkgs-spectrum'
            }
        }
        stage('Clone-em-all') {
            steps {
                sh 'git clone https://github.com/NixOS/nixpkgs'
                sh 'git clone https://github.com/tiiuae/spectrum'
                sh 'git clone https://github.com/tiiuae/nixpkgs-spectrum'
            }
        }
        stage('Dep-Check') {
            steps {
                sh '/usr/bin/dependency-check.sh --project "NixPkgs" --scan "nixpkgs/"'
                sh '/usr/bin/dependency-check.sh --project "Spectrum" --scan "spectrum/"'
                sh '/usr/bin/dependency-check.sh --project "NixPkgs-Spectrum" --scan "nixpkgs-spectrum"'
            }
        }
    }
}
