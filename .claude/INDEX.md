# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (203)

```
 10430  GET              /                                                dashboard
 14950  GET              /api/abo/status                                  api_abo_status
 10503  GET              /api/active-recordings                           api_active_recordings
 15021  GET              /api/activity-pulse                              api_activity_pulse
 14828  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 22210  GET/POST         /api/audio/config                                api_audio_config
 22240  POST             /api/audio/testtone                              api_audio_testtone
 14894  GET/POST         /api/auto-archive-rules                          api_archive_rules
 14918  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete
 14922  POST             /api/auto-archive-rules/run                      api_archive_rules_run
 11955  GET              /api/automation/status                           api_automation_status
 11977  POST             /api/automation/toggle                           api_automation_toggle
 13755  GET              /api/azrael/agents                               api_azrael_agents
 11847  POST             /api/azrael/ask                                  api_azrael_ask
 22446  GET/POST         /api/azrael/context                              api_azrael_context
 13430  GET              /api/azrael/core                                 api_azrael_core
 22580  POST             /api/azrael/live_pause                           api_azrael_live_pause
 22570  GET              /api/azrael/live_status                          api_azrael_live_status
 22588  POST             /api/azrael/live_test                            api_azrael_live_test
 13764  GET              /api/azrael/memories                             api_azrael_memories
 22636  POST             /api/azrael/persona                              api_azrael_persona_set
 22627  GET              /api/azrael/personas                             api_azrael_personas
 22664  GET              /api/azrael/piper_status                         api_azrael_piper_status
 22419  POST             /api/azrael/react                                api_azrael_react
 22455  GET              /api/azrael/reaction                             api_azrael_reaction
 22607  GET              /api/azrael/reactions                            api_azrael_reactions
 22657  GET              /api/azrael/transcript                           api_azrael_transcript
 22542  POST             /api/azrael/tts_test                             api_azrael_tts_test
 22517  GET              /api/azrael/voices                               api_azrael_voices
 22681  GET/POST         /api/azrael/whisper_model                        api_azrael_whisper_model
 10802  GET              /api/backoff-watch                               api_backoff_watch
 14305  POST             /api/backup/run                                  api_backup_run
 14271  GET              /api/backup/status                               api_backup_status
 14260  POST             /api/backup/system                               api_backup_system
 14860  GET              /api/bandwidth/live                              api_bandwidth_live
 14813  GET              /api/bookmarks                                   api_bookmarks_list
 11065  GET              /api/brain                                       api_brain
 11002  GET              /api/brain/alarms                                api_brain_alarms
 10987  GET              /api/brain/creator                               api_brain_creator
 10964  GET              /api/brain/graph                                 api_brain_graph
 11025  GET              /api/brain/growth                                api_brain_growth
  9980  GET              /api/brain/health                                api_brain_health
 23162  GET              /api/channel/categories                          api_channel_categories
 23168  POST             /api/channel/set                                 api_channel_set
 22978  GET              /api/channels/status                             api_channels_status
 21854  POST             /api/chat/send                                   api_chat_send
 13959  GET              /api/chat/send_status                            api_chat_send_status
 10484  GET              /api/checks                                      api_checks
 22483  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 22466  GET              /api/clips                                       api_clips
 22499  POST/DELETE      /api/clips/clear                                 api_clips_clear
 22132  GET              /api/cohost                                      api_cohost
 22144  POST             /api/cohost/config                               api_cohost_config
 15329  GET              /api/community/stats                             api_community_stats
 24033  GET              /api/data/export                                 api_data_export
 22058  GET              /api/debug/threads                               api_debug_threads
 24860  GET              /api/defense/attacks                             api_defense_attacks
 24827  GET              /api/defense/crowdsec                            api_defense_crowdsec
 24845  GET              /api/defense/fail2ban                            api_defense_fail2ban
 24551  GET              /api/defense/overview                            api_defense_overview
 14367  POST             /api/discord/announce                            api_discord_announce
 14095  GET              /api/discord/clips_week                          api_discord_clips_week
 14311  GET              /api/discord/community                           api_discord_community
 13987  GET              /api/discord/invite                              api_discord_invite
 13561  GET              /api/discord/overview                            api_discord_overview
 13647  POST             /api/discord/webhook_test                        api_discord_webhook_test
 14842  GET              /api/events                                      api_events
 14142  GET              /api/events/stream                               api_events_stream
 16276  GET              /api/evolution/changelog                         api_evolution_changelog
 16261  GET              /api/evolution/history                           api_evolution_history
 16201  GET              /api/evolution/learned                           api_evolution_learned
 16223  GET              /api/evolution/proposals                         api_evolution_proposals
 16244  POST             /api/evolution/proposals/<int:pid>/dismiss       api_evolution_dismiss
 16191  POST             /api/evolution/run                               api_evolution_run
 16291  GET              /api/evolution/snapshots                         api_evolution_snapshots
 16156  GET              /api/evolution/status                            api_evolution_status
 14855  GET              /api/forecast/storage                            api_forecast_storage
 11993  GET              /api/freeai/status                               api_freeai_status
 13503  GET              /api/health                                      api_health
 14873  GET              /api/heatmap/lives/<username>                    api_heatmap_lives
 14869  GET              /api/heatmap/recordings                          api_heatmap_recordings
 22181  GET              /api/highlights                                  api_highlights
 22193  POST             /api/highlights/config                           api_highlights_config
 23019  GET              /api/kick/channel                                api_kick_channel
 23040  POST             /api/kick/channel                                api_kick_channel_set
 13230  GET              /api/kick/oauth/callback                         api_kick_oauth_callback
 13298  POST             /api/kick/oauth/disconnect                       api_kick_oauth_disconnect
 13276  POST             /api/kick/oauth/redirect                         api_kick_oauth_redirect
 13215  GET              /api/kick/oauth/start                            api_kick_oauth_start
 13255  GET              /api/kick/oauth/status                           api_kick_oauth_status
 22258  GET/POST         /api/kick/sendcheck                              api_kick_sendcheck
 22327  POST             /api/kickmod/config                              api_kickmod_config
 22372  POST             /api/kickmod/import_badwords                     api_kickmod_import_badwords
 22386  GET              /api/kickmod/learned                             api_kickmod_learned
 22413  POST             /api/kickmod/learned/clear                       api_kickmod_learned_clear
 22393  POST             /api/kickmod/learned/promote                     api_kickmod_learned_promote
 22724  POST             /api/kickmod/say                                 api_kickmod_say
 22700  POST             /api/kickmod/start                               api_kickmod_start
 22298  GET              /api/kickmod/status                              api_kickmod_status
 22711  POST             /api/kickmod/stop                                api_kickmod_stop
 10364  POST             /api/login                                       dashboard_login_submit
 15314  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard
 12356  POST             /api/marketing/config                            api_marketing_config
 12381  GET              /api/marketing/preview                           api_marketing_preview
 12391  POST             /api/marketing/send-now                          api_marketing_send_now
 12330  GET              /api/marketing/status                            api_marketing_status
 12348  POST             /api/marketing/toggle                            api_marketing_toggle
 12994  POST             /api/news/config                                 api_news_config
 12960  GET              /api/news/creators                               api_news_creators
 12971  POST             /api/news/creators/generate                      api_news_creators_generate
 13036  POST             /api/news/generate-now                           api_news_generate_now
 13031  GET              /api/news/items                                  api_news_items
 13022  GET              /api/news/preview                                api_news_preview
 12941  GET              /api/news/status                                 api_news_status
 12986  POST             /api/news/toggle                                 api_news_toggle
 15283  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 13924  GET              /api/notify/status                               api_notify_status
 13935  POST             /api/notify/test                                 api_notify_test
 10588  GET              /api/outcomes                                    api_outcomes
 23639  POST             /api/overlay/config                              api_overlay_config
 23626  POST             /api/overlay/event                               api_overlay_event
 23531  GET              /api/overlay/state                               api_overlay_state
 10621  GET              /api/profile/<username>                          api_profile
 15039  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk
 14881  GET              /api/profile/snapshots/<username>                api_profile_snapshots
 15004  GET              /api/proxy/heatmap                               api_proxy_heatmap
 14981  GET              /api/proxy/trend                                 api_proxy_trend
 12915  GET              /api/public/stats                                api_public_stats
 10464  GET              /api/pulse                                       api_pulse
 14445  GET              /api/recording-attempts                          api_recording_attempts
 21789  POST             /api/restream/<int:rid>/delete                   api_restream_delete
 21767  POST             /api/restream/<int:rid>/edit                     api_restream_edit
 21808  POST             /api/restream/<int:rid>/start                    api_restream_start
 22079  POST             /api/restream/<int:rid>/stop                     api_restream_stop
 23493  GET              /api/restream/chatfeed                           api_restream_chatfeed
 21743  POST             /api/restream/create                             api_restream_create
 13306  GET              /api/restream/deck                               api_restream_deck
 11929  GET              /api/restream/health                             api_restream_health
 23515  POST             /api/restream/layout                             api_restream_layout
 21716  GET              /api/restream/list                               api_restream_list
 11898  POST             /api/restream/report                             api_restream_report
 22092  POST             /api/restream/start_all                          api_restream_start_all
 22118  POST             /api/restream/stop_all                           api_restream_stop_all
 12104  GET              /api/restream/testpush                           api_testpush_status
 12129  POST             /api/restream/testpush                           api_testpush_run
 15414  GET              /api/restream/verify                             api_restream_verify
 14073  GET              /api/retention/preview                           api_retention_preview
 14082  POST             /api/retention/run                               api_retention_run
 14798  GET              /api/search                                      api_search
 24598  GET              /api/selftest                                    api_selftest
 21825  GET              /api/shield/stats                                api_shield_stats
 10525  GET              /api/storage                                     api_storage
 10532  POST             /api/storage/cleanup                             api_storage_cleanup
 14935  GET              /api/stream/inspect/<username>                   api_stream_inspect
 11868  GET              /api/stream/timeline                             api_stream_timeline
 13635  GET              /api/stream/transcript                           api_stream_transcript
 23781  GET              /api/streamer/compare                            api_streamer_compare
 23980  POST             /api/streamer/delete/<username>                  api_streamer_delete
 14034  GET              /api/streamer/detail                             api_streamer_detail
 24005  GET              /api/streamer/digest/<username>                  api_streamer_digest
 23885  GET              /api/streamer/dormant                            api_streamer_dormant
 23961  GET              /api/streamer/exists/<username>                  api_streamer_exists
 23840  GET              /api/streamer/journal/<username>                 api_streamer_journal
 23805  GET/POST         /api/streamer/priority/<username>                api_streamer_priority
 23865  GET              /api/streamer/watchlist                          api_streamer_watchlist
 13470  GET              /api/streamers/wall                              api_streamers_wall
 10556  GET              /api/summary/preview                             api_summary_preview
 14510  GET              /api/system                                      api_system
 15362  GET              /api/system/check_timing                         api_check_timing
 15685  GET              /api/system/config_drift                         api_config_drift
 13671  GET              /api/system/config_snapshot                      api_system_config_snapshot
 13782  GET              /api/system/preflight                            api_system_preflight
 13908  GET              /api/system/preflight_history                    api_system_preflight_history
 14207  GET              /api/system/resilience                           api_system_resilience
 14833  GET              /api/tags                                        api_tags_list
 10498  GET              /api/top                                         api_top
 10857  GET              /api/trend-7d                                    api_trend_7d
 22531  GET              /api/tts/<fn>                                    api_tts_file
 15657  GET              /api/twitch/oauth/callback                       api_twitch_oauth_callback
 15609  POST             /api/twitch/oauth/redirect                       api_twitch_oauth_redirect
 15633  GET              /api/twitch/oauth/start                          api_twitch_oauth_start
 15587  GET              /api/twitch/oauth/status                         api_twitch_oauth_status
 23667  GET              /api/upload_window                               api_upload_window
 10602  GET              /api/userstats                                   api_userstats
 13047  GET              /api/version                                     api_version
 15508  GET              /api/youtube/oauth/callback                      api_youtube_oauth_callback
 15529  POST             /api/youtube/oauth/forget                        api_youtube_oauth_forget
 15541  POST             /api/youtube/oauth/logout                        api_youtube_oauth_logout
 15466  POST             /api/youtube/oauth/redirect                      api_youtube_oauth_redirect
 15490  GET              /api/youtube/oauth/start                         api_youtube_oauth_start
 15444  GET              /api/youtube/oauth/status                        api_youtube_oauth_status
 28283  GET              /api/youtube/sendrate                            api_youtube_sendrate
 14483  GET              /archive/<int:eid>/download                      archive_download
 14540  GET              /download/<int:recording_id>                     download
 14423  GET              /health                                          health
 22027  GET              /healthz                                         healthz
 10355  GET              /login                                           dashboard_login_page
 10385  GET              /logout                                          dashboard_logout
 10392  GET              /manifest.webmanifest                            pwa_manifest
 13699  GET              /metrics                                         api_prometheus_metrics
 23476  GET              /overlay                                         overlay_page
 10416  GET              /pwa-icon-<variant>.png                          pwa_icon
 10402  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (152)

```
   176  GET              /api/ai-log                                      api_ai_log   [nc/routes/stats.py]
   146  GET              /api/ai-log/<int:entry_id>                       api_ai_log_detail   [nc/routes/stats.py]
   986  GET              /api/ai/anomalies                                api_ai_anomalies   [nc/routes/ai.py]
   726  POST             /api/ai/ask                                      api_ai_ask   [nc/routes/ai.py]
   857  POST             /api/ai/claude/save                              api_claude_save   [nc/routes/ai.py]
   837  GET              /api/ai/claude/status                            api_claude_status   [nc/routes/ai.py]
   875  POST             /api/ai/claude/test                              api_claude_test   [nc/routes/ai.py]
   799  GET              /api/ai/config                                   api_ai_config   [nc/routes/ai.py]
   339  GET              /api/ai/conversations                            api_ai_conversations_list   [nc/routes/ai.py]
   350  POST             /api/ai/conversations                            api_ai_conversations_create   [nc/routes/ai.py]
   360  GET              /api/ai/conversations/<int:conv_id>              api_ai_conversation_get   [nc/routes/ai.py]
   383  DELETE           /api/ai/conversations/<int:conv_id>              api_ai_conversation_delete   [nc/routes/ai.py]
   390  PATCH            /api/ai/conversations/<int:conv_id>              api_ai_conversation_patch   [nc/routes/ai.py]
   401  POST             /api/ai/conversations/<int:conv_id>/messages     api_ai_conversation_send   [nc/routes/ai.py]
   534  POST             /api/ai/conversations/<int:conv_id>/stream       api_ai_conversation_stream   [nc/routes/ai.py]
   632  POST             /api/ai/diagnose                                 api_ai_diagnose   [nc/routes/ai.py]
  1224  GET              /api/ai/forecast-storage                         api_ai_forecast_storage   [nc/routes/ai.py]
  1256  GET              /api/ai/health-score/<username>                  api_ai_health_score   [nc/routes/ai.py]
   323  GET              /api/ai/models                                   api_ai_models   [nc/routes/ai.py]
   939  GET              /api/ai/predict-golive/<username>                api_ai_predict_golive   [nc/routes/ai.py]
   919  POST             /api/ai/query                                    api_ai_query   [nc/routes/ai.py]
  1092  GET              /api/ai/recommendations                          api_ai_recommendations   [nc/routes/ai.py]
  1140  GET              /api/ai/report                                   api_ai_report   [nc/routes/ai.py]
  1191  GET              /api/ai/retry-advice/<username>                  api_ai_retry_advice   [nc/routes/ai.py]
  1050  GET              /api/ai/segments                                 api_ai_segments   [nc/routes/ai.py]
   894  GET              /api/ai/skills                                   api_ai_skills   [nc/routes/ai.py]
   358  GET              /api/archive                                     api_archive   [nc/routes/archive.py]
   622  DELETE           /api/archive/<int:eid>                           api_archive_delete   [nc/routes/archive.py]
   504  POST             /api/archive/<int:eid>/rename                    api_archive_rename   [nc/routes/archive.py]
   487  POST             /api/archive/bulk-delete                         api_archive_bulk_delete   [nc/routes/archive.py]
   479  GET              /api/archive/check                               api_archive_check   [nc/routes/archive.py]
   315  GET              /api/archive/duplicates                          api_archive_duplicates   [nc/routes/archive.py]
   331  POST             /api/archive/duplicates/delete                   api_archive_duplicates_delete   [nc/routes/archive.py]
   666  POST             /api/archive/index/<int:rid>                     api_archive_index_one   [nc/routes/archive.py]
   631  GET              /api/archive/search                              api_archive_search   [nc/routes/archive.py]
   651  GET              /api/archive/status                              api_archive_status   [nc/routes/archive.py]
   538  POST             /api/archive/upload                              api_archive_upload   [nc/routes/archive.py]
    33  GET/POST         /api/collections                                 api_collections   [nc/routes/collections.py]
    68  POST/DELETE      /api/collections/<int:cid>                       api_collection_modify   [nc/routes/collections.py]
   103  GET              /api/collections/<int:cid>/trackings             api_collection_trackings   [nc/routes/collections.py]
   265  POST             /api/config/restore                              api_config_restore   [nc/routes/settings.py]
   250  GET              /api/config/snapshot                             api_config_snapshot   [nc/routes/settings.py]
   173  GET              /api/cookies/age                                 api_cookies_age   [nc/routes/settings.py]
    51  GET              /api/cookies/health                              api_cookies_health   [nc/routes/settings.py]
    58  POST             /api/cookies/update                              api_cookies_update   [nc/routes/settings.py]
   194  GET              /api/db/export                                   api_db_export   [nc/routes/settings.py]
   221  POST             /api/db/import                                   api_db_import   [nc/routes/settings.py]
   181  GET              /api/db/summary                                  api_db_summary   [nc/routes/settings.py]
    61  POST             /api/donations/add                               api_donations_add   [nc/routes/money.py]
    94  GET              /api/donations/manual                            api_donations_manual   [nc/routes/money.py]
   102  POST             /api/donations/manual/<int:rid>/delete           api_donations_manual_delete   [nc/routes/money.py]
    42  POST             /api/donations/reset                             api_donations_reset   [nc/routes/money.py]
   118  GET              /api/donations/summary                           api_donations_summary   [nc/routes/money.py]
   182  GET              /api/finanzamt/entries                           api_finanzamt_entries   [nc/routes/money.py]
   202  POST             /api/finanzamt/entry                             api_finanzamt_add   [nc/routes/money.py]
   229  GET              /api/finanzamt/export.csv                        api_finanzamt_csv   [nc/routes/money.py]
    36  GET              /api/health-score                                api_health_score   [nc/routes/health.py]
   158  GET              /api/insights/activity-clock                     api_insights_activity_clock   [nc/routes/insights.py]
    33  GET              /api/insights/best-times/<username>              api_insights_best_times   [nc/routes/insights.py]
   140  GET              /api/insights/catch-rate                         api_insights_catch_rate   [nc/routes/insights.py]
   115  GET              /api/insights/growth/<username>                  api_insights_growth   [nc/routes/insights.py]
   179  GET              /api/insights/leaderboard                        api_insights_leaderboard   [nc/routes/insights.py]
    66  GET              /api/insights/reliability                        api_insights_reliability   [nc/routes/insights.py]
    89  GET              /api/insights/session-stats                      api_insights_session_stats   [nc/routes/insights.py]
   213  GET              /api/insights/storage-by-streamer                api_insights_storage_by_streamer   [nc/routes/insights.py]
   206  GET              /api/moderation/feed                             api_moderation_feed   [nc/routes/stats.py]
   250  GET              /api/ops/audit                                   api_ops_audit   [nc/routes/ops.py]
   317  GET              /api/ops/db-stats                                api_ops_db_stats   [nc/routes/ops.py]
   345  GET              /api/ops/disk-breakdown                          api_ops_disk_breakdown   [nc/routes/ops.py]
   196  GET              /api/ops/errors                                  api_ops_errors   [nc/routes/ops.py]
   263  GET              /api/ops/healthcheck                             api_ops_healthcheck   [nc/routes/ops.py]
   498  GET              /api/ops/log-tail                                api_ops_log_tail   [nc/routes/ops.py]
    63  GET              /api/ops/logtail                                 api_ops_logtail   [nc/routes/ops.py]
   161  GET              /api/ops/metrics                                 api_ops_metrics   [nc/routes/ops.py]
   144  GET              /api/ops/resource_history                        api_ops_resource_history   [nc/routes/ops.py]
   384  GET              /api/ops/version                                 api_ops_version   [nc/routes/ops.py]
   815  GET              /api/rec/classify/<int:rec_id>                   api_rec_classify   [nc/routes/recordings.py]
   897  GET              /api/rec/compress-candidates                     api_rec_compress_candidates   [nc/routes/recordings.py]
   925  GET              /api/rec/orphans                                 api_rec_orphans   [nc/routes/recordings.py]
   936  POST             /api/rec/orphans/clean                           api_rec_orphans_clean   [nc/routes/recordings.py]
   802  GET              /api/rec/quality/<int:rec_id>                    api_rec_quality   [nc/routes/recordings.py]
   864  POST             /api/rec/retention/apply                         api_rec_retention_apply   [nc/routes/recordings.py]
   851  POST             /api/rec/retention/preview                       api_rec_retention_preview   [nc/routes/recordings.py]
   832  GET              /api/rec/timeline/<username>                     api_rec_timeline   [nc/routes/recordings.py]
   477  GET/POST         /api/recordings/<int:rid>/annotations            api_recording_annotations   [nc/routes/recordings.py]
   472  POST             /api/recordings/<int:rid>/bookmark               api_recording_bookmark   [nc/routes/recordings.py]
   520  POST             /api/recordings/<int:rid>/fingerprint            api_recording_fingerprint   [nc/routes/recordings.py]
   403  GET              /api/recordings/<int:rid>/inspect                api_recording_inspect   [nc/routes/recordings.py]
   730  POST             /api/recordings/<int:rid>/label                  api_recording_label   [nc/routes/recordings.py]
   494  GET              /api/recordings/<int:rid>/manifest               api_recording_manifest   [nc/routes/recordings.py]
   457  GET/POST/DELETE  /api/recordings/<int:rid>/notes                  api_recording_notes   [nc/routes/recordings.py]
   430  GET              /api/recordings/<int:rid>/quality                api_recording_quality   [nc/routes/recordings.py]
   704  POST             /api/recordings/<int:rid>/rating                 api_recording_rating   [nc/routes/recordings.py]
   574  POST             /api/recordings/<int:rid>/restore                api_recording_restore   [nc/routes/recordings.py]
   663  POST             /api/recordings/<int:rid>/star                   api_recording_star   [nc/routes/recordings.py]
   569  POST             /api/recordings/<int:rid>/trash                  api_recording_trash   [nc/routes/recordings.py]
   502  GET              /api/recordings/<int:rid>/waveform               api_recording_waveform   [nc/routes/recordings.py]
   282  POST             /api/recordings/<int:tracking_id>/stop           api_recording_stop   [nc/routes/recordings.py]
   747  GET              /api/recordings/by-label/<label>                 api_recordings_by_label   [nc/routes/recordings.py]
   370  GET              /api/recordings/daily                            api_recordings_daily   [nc/routes/recordings.py]
   625  POST             /api/recordings/dedup-scan                       api_dedup_scan   [nc/routes/recordings.py]
   780  GET              /api/recordings/disconnects                      api_recording_disconnects   [nc/routes/recordings.py]
   765  GET              /api/recordings/labels                           api_recordings_labels   [nc/routes/recordings.py]
   326  GET              /api/recordings/list                             api_recordings_list   [nc/routes/recordings.py]
   564  POST             /api/recordings/manual/<int:mid>/stop            api_manual_stop   [nc/routes/recordings.py]
   550  GET              /api/recordings/manual/list                      api_manual_list   [nc/routes/recordings.py]
   533  POST             /api/recordings/manual/start                     api_manual_start   [nc/routes/recordings.py]
   590  GET              /api/recordings/overview                         api_recordings_overview   [nc/routes/recordings.py]
   683  GET              /api/recordings/starred                          api_recordings_starred   [nc/routes/recordings.py]
   579  GET              /api/recordings/trash                            api_trash_list   [nc/routes/recordings.py]
   306  POST             /api/schedule/add                                api_schedule_add   [nc/routes/settings.py]
   296  GET              /api/schedule/list                               api_schedule_list   [nc/routes/settings.py]
   331  POST             /api/schedule/remove                             api_schedule_remove   [nc/routes/settings.py]
    48  POST             /api/scheduler/add                               api_scheduler_add   [nc/routes/scheduler.py]
    69  POST             /api/scheduler/delete                            api_scheduler_delete   [nc/routes/scheduler.py]
    35  GET              /api/scheduler/list                              api_scheduler_list   [nc/routes/scheduler.py]
    85  POST             /api/scheduler/toggle                            api_scheduler_toggle   [nc/routes/scheduler.py]
   109  GET              /api/stats                                       api_stats   [nc/routes/stats.py]
   200  GET              /api/stats/failures-by-pattern                   api_failures_by_pattern   [nc/routes/stats.py]
   195  GET              /api/stats/tiktok-status                         api_tiktok_status   [nc/routes/stats.py]
   255  GET              /api/stats/timeline                              api_stats_timeline   [nc/routes/stats.py]
   116  GET              /api/system-resources                            api_system_resources   [nc/routes/health.py]
   219  GET              /api/trackings                                   api_trackings   [nc/routes/trackings.py]
   434  POST             /api/trackings/<int:tid>/collection              api_tracking_collection   [nc/routes/trackings.py]
   463  POST             /api/trackings/<int:tid>/max-duration            api_tracking_max_duration   [nc/routes/trackings.py]
   383  GET/POST         /api/trackings/<int:tid>/priority                api_tracking_priority   [nc/routes/trackings.py]
   396  POST             /api/trackings/<int:tid>/quick-restart           api_tracking_quick_restart   [nc/routes/trackings.py]
   492  GET              /api/trackings/<int:tid>/settings                api_tracking_settings   [nc/routes/trackings.py]
   369  GET/POST/DELETE  /api/trackings/<int:tid>/tags                    api_tracking_tags   [nc/routes/trackings.py]
   244  POST             /api/trackings/<int:tracking_id>/notes           api_tracking_notes   [nc/routes/trackings.py]
   289  POST             /api/trackings/<int:tracking_id>/pause           api_tracking_pause   [nc/routes/trackings.py]
   313  POST             /api/trackings/<int:tracking_id>/recheck         api_tracking_recheck   [nc/routes/trackings.py]
   300  POST             /api/trackings/<int:tracking_id>/resume          api_tracking_resume   [nc/routes/trackings.py]
   146  POST             /api/trackings/bulk                              api_trackings_bulk   [nc/routes/trackings.py]
   258  GET              /api/trackings/export                            api_trackings_export   [nc/routes/trackings.py]
   116  GET              /api/trackings/groups                            api_trackings_groups   [nc/routes/trackings.py]
   350  GET              /api/trackings/tags-map                          api_trackings_tags_map   [nc/routes/trackings.py]
   405  GET              /api/trackings/watchlist-export                  api_watchlist_export   [nc/routes/trackings.py]
   104  POST             /api/tunnel/set                                  api_tunnel_set   [nc/routes/ops.py]
    83  GET              /api/tunnel/status                               api_tunnel_status   [nc/routes/ops.py]
   115  POST             /api/tunnel/test                                 api_tunnel_test   [nc/routes/ops.py]
    96  POST             /api/tunnel/toggle                               api_tunnel_toggle   [nc/routes/ops.py]
   446  GET              /api/update/backups                              api_update_backups   [nc/routes/ops.py]
   412  GET              /api/update/check                                api_update_check   [nc/routes/ops.py]
   471  POST             /api/update/restart                              api_update_restart   [nc/routes/ops.py]
   451  POST             /api/update/rollback                             api_update_rollback   [nc/routes/ops.py]
   434  POST             /api/update/start                                api_update_start   [nc/routes/ops.py]
   427  GET              /api/update/status                               api_update_status   [nc/routes/ops.py]
    33  GET/POST         /api/webhooks                                    api_webhooks   [nc/routes/webhooks.py]
    73  DELETE           /api/webhooks/<int:wid>                          api_webhook_delete   [nc/routes/webhooks.py]
   104  POST             /api/webhooks/<int:wid>/test                     api_webhook_test   [nc/routes/webhooks.py]
    88  POST             /api/webhooks/<int:wid>/toggle                   api_webhook_toggle   [nc/routes/webhooks.py]
```

## Discord-Slash-Commands (45)

```
 25303  /ai                     AZRAEL / KI fragen (Text oder Sprachnachricht)
 25762  /ask                    AZRAEL etwas fragen — der KI-Community-Assistent
 25394  /assign_role            Rolle/Gruppe einem Mitglied geben
 25440  /ban                    Mitglied bannen
 26094  /botstats               Bot-Health: Uptime, Trackings, Aufnahmen, DB (Admin)
 26018  /clearwarns             Alle Verwarnungen eines Mitglieds löschen
 26058  /clip                   Highlight-Clip der letzten Sekunden vom laufenden Stream
 26043  /clipoftheweek          Aktuell führender Clip-of-the-Week (⭐-Voting)
 25885  /clips                  Letzte Highlight-Clips eines Users
 25355  /create_category        Kategorie anlegen
 25324  /create_channel         Text-Channel anlegen (optional in Kategorie)
 25383  /create_group           Nutzergruppe (= Rolle) anlegen
 25366  /create_role            Rolle / Nutzergruppe anlegen
 25340  /create_voice           Voice-Channel anlegen
 25676  /daily                  Tägliche XP-Belohnung abholen (Streak-Bonus!)
 25792  /event                  Community-Event ankündigen (Admin) — mit Countdown
 25835  /events                 Kommende Community-Events anzeigen
 25931  /follow                 Bei Live-Gang eines Streamers gepingt werden
 25915  /help                   Alle Bot-Befehle anzeigen
 25429  /kick                   Mitglied kicken
 25658  /leaderboard            Top-10 der Community nach XP
 25871  /livenow                Welche getrackten User sind gerade live
 25901  /post_test              Test: Nachricht in den Channel eines getrackten Users posten
 25732  /profile                Dein Community-Profil: Level, Rang, Streak, Rang-Platz
 25464  /purge                  Letzte N Nachrichten im Channel löschen (max 100)
 25644  /rank                   Dein Level und Rang anzeigen
 25858  /recstatus              Aktuell laufende Aufnahmen
 25405  /remove_role            Rolle/Gruppe entfernen
 25317  /restream_status        Restream-Status
 25416  /set_channel_perms      Rechte einer Rolle für einen Channel setzen
 25609  /setup_community        Community-Server einrichten: Ränge, Channels, Rechte
 25627  /setup_targets          Pro getracktem User: Clips-, Chat- und Voice-Channel anlegen
 25957  /stats                  Statistik zu einem getrackten Streamer
 25229  /status                 Azrael Sentinel Status: Trackings, Live, Restream
 26253  /streaminfo             Kompakt-Karte eines Streamers: Aktivität, Aufnahmen, Followe
 26150  /sys_report             Azrael Sentinel Wochenreport (Brain, Markdown)
 26126  /sys_unpause            Auto-pausierte Quelle wieder aktivieren (Admin)
 25451  /timeout                Mitglied stummschalten (Minuten)
 26029  /topstreamers           Rangliste der Streamer nach Aufnahmen
 25259  /track                  TikTok-User tracken
 25243  /tracklist              Getrackte TikTok-User dieses Servers
 25946  /unfollow               Live-Pings für einen Streamer abbestellen
 25292  /untrack                TikTok-User nicht mehr tracken
 25979  /warn                   Mitglied verwarnen (eskaliert ab 3 Verwarnungen zu Timeout)
 26003  /warnings               Verwarnungen eines Mitglieds anzeigen
```

## Discord-Events (4)

```
 26737  on_member_join
 26699  on_message
 26340  on_raw_reaction_add
 26772  on_ready
```

## Top-Level-Symbole in bot.py (553 Funktionen, 2 Klassen)

```
  2477-2478   _abo_key
  2498-2516   _abo_probe_dump
 24140-24150  _active_recorder_sync
 19013-19020  _ad_allowlist
 20135-20141  _agent_for
 24152-24170  _ai_calls_total_sync
 20144-20160  _ai_telemetry
 20642-20660  _alert
 26885-26935  _alert_monitor_loop
 27314-27376  _announce_loop
  3419-3422   _anthropic_key
  3429-3431   _anthropic_model
 10108-10111  _arg_int
  2469-2474   _as_dict
 16873-16878  _audio_cfg
 20796-20818  _audio_tap_cmd
 10276-10287  _auth_cookie
 10243-10272  _auth_guard
  1625-1630   _auto_on
 21692-21710  _auto_restream_loop
 28444-28459  _azrael_broadcast_reply
 28344-28366  _azrael_chat_reply
 28327-28341  _azrael_chat_should_reply
 12612-12630  _azrael_creator_take
 28372-28374  _azrael_gate_cfg
 20165-20179  _azrael_live_state
 23379-23393  _azrael_overlay_state
 20525-20579  _azrael_proactive_loop
 19984-20040  _azrael_reaction_to_chats
 28377-28384  _azrael_reply_all_chats
 28314-28324  _azrael_self_names
 28412-28441  _azrael_send_to
 20182-20203  _azrael_system
 27054-27057  _backup_active
 27135-27148  _backup_loop
 18901-18902  _badwords_path
 26850-26859  _brain_growth_loop
 10933-10960  _brain_growth_snapshot
  2405-2425   _brain_hint_delay
 10925-10927  _brain_history_for
  6508-6536   _brain_notify
 10902-10923  _brain_record
 10929-10931  _brain_stream_recent
 14121-14138  _browser_push
  6552-6639   _build_daily_summary
  2908-3088   _build_native_cmd
 17221-17408  _build_restream_cmd
  3132-3165   _build_ytdlp_cmd
 24092-24099  _cached_probe
  5330-5357   _can_stop_tracking
  1805-1827   _capture_set_cookies
 15098-15101  _cfg_get
 15104-15106  _cfg_set
 23123-23158  _channel_set_all
 16471-16474  _chat_connected
 16477-16493  _chat_disconnected
  8588-8599   _chat_is_forum
 16513-16515  _chat_sanitize
 16517-16526  _chat_src_ok
 16456-16468  _chat_stat
 16496-16499  _chat_stats_snapshot
  3694-3705   _check_ai_alive_sync
  3708-3720   _check_ai_models_sync
 24101-24114  _check_redis_alive_sync
 24116-24136  _check_redis_version_sync
 13999-14012  _ci_key
 11532-11575  _classify_pool_anonymity
 11578-11595  _classify_pool_anonymity_bg
   782-786    _claude_chat_sync_metered
 10137-10144  _client_ip
 27408-27435  _clip_prune
 27438-27448  _clip_recfile_for
 27964-27970  _clip_should_velocity
 27489-27571  _clip_to_discord
  3592-3601   _close_ai_session
 28488-28503  _cohost_broadcast
 28470-28474  _cohost_cfg
 28529-28541  _cohost_fire_highlight
 28477-28485  _cohost_gate
 28506-28526  _cohost_highlight
 27620-27654  _community_events_loop
 10756-10758  _conv_messages
  6938-6978   _cookie_alarm_loop
  1877-1881   _cookie_autorefresh_info
  1782-1786   _cookie_header
 14171-14203  _cpu_load_snapshot
  3902-3914   _create_index_safe
 12580-12595  _creator_activity
 12636-12659  _creator_dossier_generate
 12598-12609  _creator_facts_line
 24353-24459  _crowdsec_status
 24319-24350  _crowdsec_via_lapi
 24184-24202  _cscli_bin
 24208-24221  _cscli_path
  6831-6856   _daily_summary_loop
 24239-24256  _darf_journal_lesen
 26862-26882  _db_maintenance_loop
  6800-6828   _db_vacuum_loop
 19036-19060  _detect_foreign_ad
  1363-1374   _diag_path_owner
 20431-20475  _director_finalize
 21242-21249  _director_for
 20380-20428  _director_mark
 27858-27893  _disc_automod_check
 27831-27837  _disc_state_get
 27840-27847  _disc_state_set
 24902-24915  _discord_guild_filesize_bytes
 25101-25110  _discord_invite
 27792-27828  _discord_live_thread
 20582-20594  _discord_notify
 25002-25027  _discord_ops_alert
 27690-27788  _discord_post_user
 25166-26847  _discord_run_once
 25040-25098  _discord_start
 27379-27385  _discord_stop
 24923-24925  _discord_upload_limit_label
 24918-24920  _discord_upload_limit_mb
  6859-6933   _disk_alarm_loop
 29879-29928  _disk_autoclean
 29931-29944  _disk_guard_loop
 29871-29876  _disk_pct
 16830-16832  _drawtext_chain
 14637-14639  _dump_all_threads
 11457-11521  _enrich_proxies_with_geo
  2022-2066   _ensure_cookie_file_netscape
 25113-25163  _ensure_discord_invite
 27585-27617  _ensure_error_channel
  8647-8650   _ensure_notify_topic
 11700-11737  _ensure_proxy_ready
  8601-8628   _ensure_topic
   645-647    _env_int
   650-652    _env_int_range
 27657-27687  _error_channel_loop
 20626-20639  _event_webhook
 15764-15770  _evo_build_dir
 15773-15780  _evo_version
 16056-16137  _evolution_cycle
 15789-15809  _evolution_llm_note
 16140-16150  _evolution_loop
 15812-16053  _evolution_write_build
  5950-5984   _extract_file_payload
  2154-2156   _extract_urls_from_streamurl_node
 24224-24231  _f2b_sudo_hint
 20662-20664  _faster_whisper_available
 18925-18937  _fetch_ldnoobw_de
 11346-11364  _fetch_proxy_list
 21076-21104  _fetch_tiktok_room_id
   716-719    _ff_cmd
 16993-16998  _find_chromium
  3125-3129   _find_external_recorder
  2159-2161   _find_stream_urls
 15149-15174  _fire_webhooks
  7714-7723   _fork_safe
   797-806    _freeai_chat_sync_metered
 24274-24316  _geo_lookup_ips
  3581-3590   _get_ai_session
  7548-7588   _get_live_info
  2695-2702   _get_resolve_semaphore
  7949-8315   _handle_single_tracking
 29723-29725  _hb
 29728-29745  _hb_while
 16531-16533  _highlight_cfg
 16536-16565  _highlight_observe
 17001-17006  _htmlov_screenshot_cmd
 20820-20830  _httpx_proxy
 15182-15194  _in_quiet_hours
 30758-30789  _install_fast_eventloop
 10003-10057  _install_fast_json
 14642-14658  _install_faulthandler
 21935-21944  _intel_ensure_schema
 21982-22017  _intel_index_loop
 21956-21966  _intel_index_one
 21947-21953  _intel_semantic
  5319-5328   _is_authorized
  7879-7885   _is_dead
  2144-2146   _is_hevc
 24259-24265  _is_private_ip
  1527-1534   _is_process_running
  6538-6549   _is_quiet_hours
  1164-1173   _is_upload_window
 10092-10105  _json_error_handler
  6758-6788   _kick_broadcaster_id
 12030-12049  _kick_channel_live
  6672-6714   _kick_follower_count
 13193-13206  _kick_oauth_exchange
 13209-13211  _kick_oauth_page
 13152-13156  _kick_redirect_public
 13147-13149  _kick_redirect_source
 13139-13144  _kick_redirect_uri
  6657-6659   _kick_slug
 13159-13190  _kick_user_token
  3951-3954   _kind_from_filename
 15211-15216  _latest_popularity
 18947-18953  _learned_load
 18944-18945  _learned_path
 18955-18963  _learned_save
 21457-21487  _live_react_loop
 21253-21446  _live_react_worker
 20043-20054  _live_transcript_push
 21448-21455  _live_users
 20478-20522  _living_title_loop
 18904-18912  _load_banned_words_file
  1703-1776   _load_cookies_dict
 27060-27132  _local_backup_scan
 10074-10088  _log_5xx
 17416-17428  _looks_like_codec_err
 17411-17413  _looks_like_source_expired
  7795-7825   _loop_fehler
 14662-14671  _loop_heartbeat
 29693-29720  _loop_lag_monitor
 14781-14784  _loop_not_ready
 14674-14742  _loop_watchdog_thread
 19923-19937  _loyalty_add
 19914-19920  _loyalty_get
 19940-19948  _loyalty_top
 15348-15350  _manual_donations_total
  7887-7888   _mark_dead
 12197-12226  _marketing_cfg
 12188-12194  _marketing_default_targets
 12183-12185  _marketing_enabled
 12240-12255  _marketing_flavor
 12310-12326  _marketing_loop
 12258-12268  _marketing_post_discord
 12271-12283  _marketing_post_telegram
 12286-12307  _marketing_publish
 12229-12233  _marketing_state_obj
 12236-12237  _marketing_state_save
 28391-28409  _maybe_handle_command
 30030-30054  _maybe_hype_clip
  3869-3892   _migrate_columns
 28668-28679  _mod_is_exempt
 28682-28687  _mod_warn_first
 28690-28693  _mod_warn_text
 16319-16327  _modlog
   917-919    _multistream_targets
  7726-7727   _nc_create_subprocess_exec
  7730-7731   _nc_create_subprocess_shell
 12662-12679  _news_absaetze
 12421-12437  _news_cfg
 12408-12410  _news_enabled
 12475-12572  _news_facts
 12713-12735  _news_generate
 12920-12937  _news_loop
 12413-12418  _news_output_path
 12575-12577  _news_phrase
 12682-12710  _news_phrase_impl
 12450-12457  _news_read
 12440-12443  _news_state_obj
 12446-12447  _news_state_save
 12460-12472  _news_write
 16357-16359  _normalize_ingest
  2336-2353   _note_check_duration
  8641-8644   _notify_topic_name
 13103-13114  _oauth_redirect_env
 13130-13136  _oauth_redirect_source
 13117-13127  _oauth_redirect_uri
 20069-20077  _oracle_memories
 20335-20369  _oracle_memorize
 20080-20093  _oracle_persona
 20062-20066  _oracle_recent_text
 16656-16664  _ov_atomic_write
 16644-16650  _ov_bar
 18860-18872  _ov_clip_text
 16653-16654  _ov_oneline
 23443-23472  _overlay_push
 16947-16990  _overlay_render_size
 16418-16422  _overlay_session_reset
 23395-23398  _overlay_src_ok
 19023-19033  _own_invites
 16942-16944  _parse_size
 24467-24547  _parse_ssh_attacks
  7150-7183   _pause_resume_cmd
  1831-1875   _persist_refreshed_cookies
  1669-1701   _pick_checked_pull_proxy
 10173-10186  _pin_auth_value
 10232-10233  _pin_clear_fail
 10212-10215  _pin_locked
 10218-10229  _pin_note_fail
 10189-10209  _pin_ok
 23285-23287  _piper_available
 23250-23272  _piper_list_voices
 23292-23317  _piper_pick_model
 23329-23376  _piper_say
 23243-23247  _piper_voice_roots
 15111-15146  _post_json_threaded
 16921-16939  _probe_video_size
  1555-1572   _proc_is_recorder
 11444-11455  _proxy_geo_cache_put
 11671-11697  _proxy_pool_refresh_loop
  1635-1666   _proxy_report_recording
 14627-14629  _prune_stall_dumps
 13062-13100  _public_base_url
 12738-12859  _public_stats
 20597-20623  _push_notify
 10334-10336  _pwa_dir
 11415-11430  _quick_validate_proxy
 15177-15179  _quiet_hours_config
 10299-10332  _rate_guard
 19888-19894  _react_warn
  7634-7673   _reap_proc
  2376-2398   _record_check_outcome
   711-713    _redact_stream_urls
 11598-11668  _refresh_proxy_pool
 23275-23281  _resolve_piper_model
 14015-14030  _resolve_tracked_user
  2170-2260   _resolve_via_html
  2518-2672   _resolve_via_webcast_api_v2
  2735-2797   _resolve_via_ytdlp
 28010-28139  _resolve_youtube_ingest
 21526-21533  _restream_active_platforms
 16403-16414  _restream_active_sources
 21107-21206  _restream_chat_guardian
 16568-16640  _restream_chat_push
 16330-16342  _restream_enabled
 17009-17096  _restream_html_overlay_start
 17099-17112  _restream_html_overlay_stop
  1112-1114   _restream_layout_mode
 16368-16391  _restream_overlay_files
 21491-21523  _restream_platform_state
 21654-21689  _restream_resume_after_restart
 17160-17218  _restream_tts_enqueue_wav
 16883-16915  _restream_tts_feeder
 16880-16881  _restream_tts_fifo_path
 17115-17142  _restream_tts_start
 17144-17158  _restream_tts_stop
 21536-21651  _restream_verify_loop
 27025-27037  _retention_loop
 26984-27022  _retention_scan
  2480-2482   _room_is_abo
  5988-6105   _run_ai_call
 14765-14778  _run_async_from_flask
 24268-24271  _run_priv
 30746-30754  _run_selfcheck_and_exit
 27040-27051  _s3_client
  7890-7936   _safe_send
  4583-4599   _sample_net_throughput
 18914-18922  _save_banned_words_file
  2428-2455   _schedule_next_check
 26938-26981  _scheduler_loop
  3895-3899   _schema_pk
 14786-14791  _scraper_session
 28696-28735  _screen_full
 13519-13556  _sec_headers
  2149-2151   _select_stream_from_data_section
 30559-30743  _selfcheck
  8653-8687   _send_live_notice
  1187-1191   _should_defer_upload
 27451-27486  _shrink_for_discord
 10339-10351  _sicheres_ziel
 29951-29968  _sign_health_check
 29971-29990  _sign_health_loop
  7743-7754   _spawn
  7757-7787   _spawn_from_flask
 24591-24594  _st_befund
 20832-21073  _start_chat_listener
 14745-14762  _start_loop_watchdog
 12883-12911  _stats_loop
 12862-12865  _stats_output_path
 12868-12880  _stats_write
  8383-8397   _storage_cleanup_loop
 30010-30017  _story_for
  3187-3193   _stream_url_expiry
  3202-3208   _stream_url_is_fresh
  3195-3200   _stream_url_ttl
 18987-18994  _streamer_persona_get
 18969-18975  _streamer_personas_load
 18966-18967  _streamer_personas_path
 18977-18985  _streamer_personas_save
 16835-16839  _studio_chain
 27157-27279  _system_backup
 27282-27310  _system_backup_loop
 11367-11406  _test_proxy
 12071-12080  _testpush_cfg
 12083-12100  _testpush_exec
 12052-12068  _testpush_resolve_live
  8560-8570   _tg_topics_load_into_mem
  8557-8558   _tg_topics_path
  8572-8579   _tg_topics_save
 23909-23957  _tiktok_account_exists
 10147-10155  _token_ok
  8582-8586   _topic_forget
 15197-15208  _tracking_max_duration
  4201-4213   _tracking_resume_cleanup
  1421-1444   _try_attach_file_handler
 23319-23327  _tts_cleanup
 12008-12012  _tunnel_effective
 22745-22798  _twitch_channel_status
 28738-28881  _twitch_chat_loop
 28552-28655  _twitch_eventsub_loop
 15678-15681  _twitch_oauth_page
  1210-1223   _upload_queue_add
  1234-1236   _upload_queue_count
  1193-1202   _upload_queue_load
  1183-1185   _upload_queue_path
  1225-1232   _upload_queue_remove
  1204-1208   _upload_queue_save
  1238-1279   _upload_window_loop
  7607-7614   _uptime_s
 16345-16354  _url_host
   691-708    _url_ohne_zugang
   775-779    _usage_record_claude
  7828-7872   _verbindung_verloren
  6717-6748   _viewer_sample_loop
  6790-6797   _viewer_stats
 10236-10239  _wants_html
  7617-7631   _warn_empty_env
 29766-29861  _watchdog_loop
 28293-28301  _wchat_thank_ok
 20666-20696  _whisper_get_model
  7704-7711   _whisper_native_section
 19875-19881  _whisper_pool
 20765-20794  _whisper_segments
 20698-20762  _whisper_transcribe
 16666-16828  _write_restream_overlay
 28909-28988  _youtube_api_chat_loop
 22801-22904  _youtube_api_status
 22907-22974  _youtube_channel_status
 28991-29151  _youtube_chat_loop
 28145-28158  _youtube_restream_autoconfig
 28161-28185  _youtube_restream_autoconfig_inner
 28251-28279  _youtube_send
 23079-23120  _youtube_set_channel
 28188-28222  _yt_access_token
 28225-28240  _yt_live_chat_id
 28902-28906  _yt_oauth_configured
 28246-28248  _yt_sendrate_cfg
 28884-28899  _yt_timeout
  2719-2720   _ytdlp_detect_available
  2722-2733   _ytdlp_note_result
 14632-14634  _zombie_child_count
  7484-7508   about
  4070-4074   add_ai_log_entry
  3987-3990   add_archive_entry
  4696-4711   add_archive_rule
  4372-4406   add_recording
  4135-4152   add_tracking
  6108-6141   ai
  3734-3773   ai_chat
  3807-3817   ai_history_append
  3819-3824   ai_history_clear
  3796-3805   ai_history_load
  3781-3794   ai_rate_limit_check
  6170-6178   aireset
 20206-20225  azrael_chat
 29156-29278  brain_cmd
  3211-3395   build_recording_cmd
  4155-4158   bulk_add_trackings
  6981-7040   bulkadd
  8400-8540   check_all_trackings
  4217-4229   claim_live_transition
 19063-19818  class KickModerator
 17431-18747  class RestreamManager
 11782-11824  classify_proxy_anonymity
  6216-6414   cleanup
  5179-5220   cleanup_old_recordings
  4363-4370   clear_recording
 27896-27961  clip_moment
  4527-4576   compute_storage_forecast
  7103-7147   cookies_cmd
  4126-4132   count_trackings_for_chat
  4057-4068   decide_preferred_recorder
  3997-4000   delete_archive_entry
  4713-4721   delete_archive_rule
  5645-5792   diag
 29390-29451  einnahmen_cmd
  4521-4524   find_recordings_by_fingerprint
  4018-4034   finish_recording_attempt
  4189-4191   get_all_active_trackings
  4085-4088   get_all_checks
  4408-4411   get_all_recordings
  4470-4472   get_all_tags_with_counts
  4498-4501   get_annotations_for_recording
  3992-3995   get_archive_entry
  4491-4494   get_bookmarked_recordings
  1898-2015   get_cookie_health
  4458-4464   get_event_log
  4041-4055   get_last_recording_attempt
  2800-2905   get_live_status
  4979-4982   get_manual_recordings
  4506-4509   get_or_compute_inspect_sync
  5255-5299   get_outcome_breakdown
  4477-4480   get_priority_poll_interval
  4674-4683   get_profile_snapshots
  4036-4039   get_recent_recording_attempts
  4413-4416   get_recording_by_id
  4484-4487   get_recording_note
  3529-3552   get_redis
  4115-4118   get_stats
  5146-5177   get_storage_stats
  4814-4816   get_tiktok_status_distribution
  4231-4240   get_tracking_state
  4186-4187   get_trackings_for_group
  4995-4998   get_trash_recordings
  9308-9971   handle_recording_finished
  3917-3942   init_db
  5069-5123   inspect_stream_url
 23438-23440  is_revenue_platform
  4686-4694   list_archive_rules
  5449-5487   live
  7939-7947   live_check_worker
  3604-3638   llm_chat
  3661-3689   llm_chat_sync
  3646-3658   llm_list_models
  4424-4450   log_event
  1489-1522   log_recording_failure
  7297-7346   logs_cmd
 30058-30549  main
  6144-6167   on_ai_media
  7423-7449   on_ai_reply
  7452-7481   on_azrael_mention
  7513-7543   on_callback
 20228-20332  oracle_handle
  7186-7189   pause_tracking
  5309-5314   profile_keyboard
  7248-7294   quota
  8317-8380   reaper_loop
  4810-4812   record_tiktok_status
  6183-6213   recstatus
  3554-3562   redis_get_json
  3564-3570   redis_set_json
  4160-4184   remove_tracking
 29454-29464  report_cmd
 11827-11829  report_proxy_result
  2263-2290   resolve_tiktok_live_stream
  4990-4993   restore_recording
  7192-7195   resume_tracking
  4724-4804   run_archive_rules
 29467-29673  run_bot
 14554-14601  run_flask
  4602-4647   sample_bandwidth_for_active
  4653-4672   save_profile_snapshot
  4077-4083   save_tiktok_check
  4355-4361   set_recording_file
  4194-4198   set_tracking_paused
  4985-4988   soft_delete_recording
  8693-9306   split_and_send_video
  5362-5404   start
  4002-4016   start_recording_attempt
  6417-6455   stats
  4960-4977   stop_manual_recording
  7198-7245   stoprec
  6642-6650   summary_cmd
  7349-7420   sysres
  5794-5938   teststream
  5406-5447   tiktok
  7043-7100   topusers
  5524-5581   track
  5489-5521   track_exact
  5595-5643   tracklist
  4826-4958   trigger_manual_recording
  4316-4353   try_acquire_recording_lock
  5001-5060   universal_search
  5583-5593   untrack
 29281-29387  update_cmd
  4516-4519   update_recording_fingerprint
```

## nc/ — öffentliche Symbole

```
__init__.py            —
abo.py                 room_is_abo
admod.py               build_allowlist
aidb.py                add_log_entry, conv_messages
archive.py             add_archive_entry, compute_recording_fingerprint, configure, delete_archive_entry, evaluate_archive_rule, get_archive_entries_paged, get_archive_entry, run_archive_file_check
archivename.py         open_unique
audio_cue.py           cue_pcm, duck_ratio, mix_chain, silence_pcm, tone_pcm
binresolve.py          resolve
cfgnorm.py             normalize_audio, normalize_cohost, normalize_gate, normalize_highlights, normalize_quiet_hours, normalize_sendrate
cfgstore.py            get, set_, upsert
channels.py            configure_chat
chatstats.py           summarize
claude.py              api_key, build_payload, chat_sync, is_retired, model, model_raw, parse_response, parse_usage, probe, resolve_model, test_key
cohost.py              decide, default_config, new_state, prompt_seed, snapshot
community.py           configure, highlight_post, live_ping, note_chatter, seen_stats
confdrift.py           config_drift, extract_defaults, log_watchlist_drift
convmap.py             messages
cookies.py             —
creatoragg.py          summarize
crowdsec.py            base_url, decisions_url, explain_status, headers, parse_decisions
crypto.py              addresses, snapshot
ctx.py                 class Ctx, configure, get, is_configured
dbexport.py            db_export_sql, db_import_sql, export_summary, parse_header
dbwrap.py              configure_db, db_conn, get_pool, set_pool
director.py            class LiveDirector, configure
discordlimits.py       describe, effective_upload_mb, gate_mb, guild_limit_mb
donations.py           configure, fmt_eur, parse_number, source_allowed, to_eur, unknown_count
donationsdb.py         manual_rows, manual_total, parse_eur
envnum.py              clamp_float, clamp_int, env_float, env_int, env_int_range
eventquery.py          build_query
evolution.py           analyze
ffbuild.py             ff_cmd
ffdiag.py              clip_caption_escape, ffprobe_duration, redact_cmd_for_log
ffmpeg_filters.py      drawtext_chain, studio_chain
ffver.py               parse_version
filepayload.py         classify_downloaded, size_reject
flapguard.py           class FlapConfig, class FlapUrteil, class FlapWatch
fmt.py                 fmt_duration, fmt_size_mb, pre_table, utc_clock
freeai.py              alive_sync, bases_status, chat, chat_stream, chat_sync, configure, diagnose, last_errors, list_models_sync
highlights.py          check, new_state, observe, score
inspectcache.py        parse_row, serialize
journalperm.py         may_read
kick_oauth.py          build_authorize_url, gen_pkce, gen_state, has_scope, is_expired, parse_token_response, token_exchange_payload, token_refresh_payload
ledger.py              add_entry, class LedgerError, crosscheck, ensure_schema, entries, export_csv, summary, verify_chain
logfilters.py          configure_logfilters
loginpage.py           login_page
logsafe.py             redact_stream_urls
loyalty.py             award_chat, award_return, configure, leaderboard, rank_for, status
marketing.py           class MarketingConfig, class MarketingState, compose, has_content, next_due_ts, should_post, variants
modheuristics.py       caps_ratio, count_links, count_mentions, escalation_minutes, escalation_step, flood_reason, is_caps_spam, is_exempt, kick_roles, prune_history, prune_infractions, resolve_exempt, stateless_reason, twitch_roles
netstat.py             sum_bytes, throughput_kbps
news.py                build_items, class NewsConfig, class NewsState, item_id, merge, render_json, should_generate
notes.py               add_annotation, delete_annotation, set_recording_note, set_tracking_notes, toggle_bookmark
oauthpage.py           kick, twitch
persona.py             —
piper_voices.py        resolve_model_path, voice_roots
preflight.py           configure
procdiag.py            dump_all_threads, prune_stall_dumps, zombie_child_count
proxyutil.py           class ProxyHealth, configure_proxy_select, configure_proxyhealth, configure_router, get_random_proxy, proxy_pool, record_proxy, tunnel_effective, tunnel_state
qrsvg.py               qr_svg
recdb.py               configure, find_recordings_by_fingerprint, get_all_recordings, get_annotations_for_recording, get_bookmarked_recordings, get_manual_recordings, get_or_compute_inspect_sync, get_recent_recording_attempts, get_recording_by_id, get_recording_note, get_trash_recordings, restore_recording, soft_delete_recording, update_recording_fingerprint
recdiag.py             class RateConfig, class RateSpur, disconnect_analysis, url_refresh_stats
replygate.py           allow, default_config
restream_guard.py      class GuardConfig, class RestreamGuard, class RestreamState, class TargetState, classify
restream_stability.py  budget_after_run, budget_exhausted, class ReconnectPolicy, class StallVerdict, expired_delay, expired_is_spinning, expired_streak, is_codec_failure, looks_like_network_failure, reconnect_delay, stall_verdict
restream_targets.py    active_targets, build_output_args, configure, multistream_targets, single_output_args
restream_testpush.py   build_cmd, class GuardDecision, class ResolvedTarget, class TestPushConfig, classify_result, fingerprint, guard, resolve_target
restream_util.py       looks_like_source_expired, normalize_ingest
restrend.py            rising_trend
schema.py              create_schema
scoring.py             build_report, compute_quality_score
scraper.py             class TikTokScraper, configure_scraper
sendrate.py            allow, default_config, new_state, snapshot
shield.py              —
sqlguard.py            check_readonly, normalize, with_limit
sqlutil.py             —
stats.py               configure_stats, get_activity_pulse, get_lives_heatmap, get_per_user_stats, get_recordings_heatmap, get_stats, get_tiktok_status_distribution, invalidate_stats_cache
story.py               class StoryMemory, configure
streamsel.py           extract_urls_from_streamurl_node, find_stream_urls, is_hevc, select_stream_from_data_section
sysload.py             classify_load, parse_meminfo, parse_ps
sysrun.py              run_priv
textmore.py            configure_banned_cap, split_for_telegram
textutil.py            clean_username, fmt_number, is_valid_tiktok_username, safe, short
trackingdb.py          add_tracking_tag, bulk_add_trackings, claim_transition, configure, get_all_active_trackings, get_all_tags_with_counts, get_priority_poll_interval, get_state, get_tags_for_tracking, get_tracking_priority, get_trackings_for_group, remove_tracking_tag, set_tracking_paused, set_tracking_priority
twitchoauth.py         access_token, authorize_url, configure, exchange_code, login_name, search_category, status, timeout_user, update_channel
updater.py             build_plan, check, class Plan, class UpdaterConfig, configure, describe, download_zip, is_protected, job_state, list_backups, local_head, local_state, normalize, remote_head, repo_url, rollback, run_update, settings, sha256_bytes, sha256_file, short_sha, start_update, strip_archive_root, zip_url
usage.py               configure, estimate_tokens, flush, record, snapshot
util.py                —
version.py             changelog, current, latest, summary_line
youtube_api.py         active_broadcast_params, ban_payload, is_self, list_params, merge_video_snippet, parse_broadcast_id, parse_error, parse_messages, parse_video_snippet, video_list_params, video_update_body
ytoauth.py             access_token, authorize_url, configure, exchange_code, forget, invalidate_access, revoke, set_channel, status
```

## brain/ — öffentliche Symbole

```
__init__.py            class Brain, get_brain
agents.py              class Agent, class AgentManager, class AnalyticsAgent, class DiskAgent, class HealthAgent, class LearningAgent, class ProxyHealthAgent, class RecordingAgent, class RecoveryAgent, class RestreamSentinelAgent, class ScoutAgent, class SentinelAgent, class SwapAgent, class ToxicityAgent, class UptimeAgent
knowledge.py           class KnowledgeGraph
llm.py                 class BudgetExhausted, class LLMRuntime
memory.py              class Memory
report.py              weekly
router.py              class Task, class TaskRouter, class Unhandled
rules.py               class Rule, class RulesEngine
scheduler.py           class Scheduler
semantic.py            class SemanticMemory
state.py               class Entity, class StateMachine
test_bughunt.py        db_conn, main
test_m1.py             main
test_m3.py             main
test_m4.py             main
test_m5.py             main
test_m6.py             class LlamaCppMock, main
test_m7.py             db_conn, main
```
