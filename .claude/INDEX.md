# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (172)

```
 10436  GET              /                                                dashboard
 14307  GET              /api/abo/status                                  api_abo_status
 10509  GET              /api/active-recordings                           api_active_recordings
 14378  GET              /api/activity-pulse                              api_activity_pulse
 14185  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 21063  GET/POST         /api/audio/config                                api_audio_config
 21093  POST             /api/audio/testtone                              api_audio_testtone
 14251  GET/POST         /api/auto-archive-rules                          api_archive_rules
 14275  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete
 14279  POST             /api/auto-archive-rules/run                      api_archive_rules_run
 11963  GET              /api/automation/status                           api_automation_status
 11985  POST             /api/automation/toggle                           api_automation_toggle
 13182  GET              /api/azrael/agents                               api_azrael_agents
 11855  POST             /api/azrael/ask                                  api_azrael_ask
 21299  GET/POST         /api/azrael/context                              api_azrael_context
 12887  GET              /api/azrael/core                                 api_azrael_core
 21433  POST             /api/azrael/live_pause                           api_azrael_live_pause
 21423  GET              /api/azrael/live_status                          api_azrael_live_status
 21441  POST             /api/azrael/live_test                            api_azrael_live_test
 13191  GET              /api/azrael/memories                             api_azrael_memories
 21489  POST             /api/azrael/persona                              api_azrael_persona_set
 21480  GET              /api/azrael/personas                             api_azrael_personas
 21517  GET              /api/azrael/piper_status                         api_azrael_piper_status
 21272  POST             /api/azrael/react                                api_azrael_react
 21308  GET              /api/azrael/reaction                             api_azrael_reaction
 21460  GET              /api/azrael/reactions                            api_azrael_reactions
 21510  GET              /api/azrael/transcript                           api_azrael_transcript
 21395  POST             /api/azrael/tts_test                             api_azrael_tts_test
 21370  GET              /api/azrael/voices                               api_azrael_voices
 21534  GET/POST         /api/azrael/whisper_model                        api_azrael_whisper_model
 10808  GET              /api/backoff-watch                               api_backoff_watch
 13666  POST             /api/backup/run                                  api_backup_run
 13632  GET              /api/backup/status                               api_backup_status
 13621  POST             /api/backup/system                               api_backup_system
 14217  GET              /api/bandwidth/live                              api_bandwidth_live
 14170  GET              /api/bookmarks                                   api_bookmarks_list
 11071  GET              /api/brain                                       api_brain
 11008  GET              /api/brain/alarms                                api_brain_alarms
 10993  GET              /api/brain/creator                               api_brain_creator
 10970  GET              /api/brain/graph                                 api_brain_graph
 11031  GET              /api/brain/growth                                api_brain_growth
  9986  GET              /api/brain/health                                api_brain_health
 22015  GET              /api/channel/categories                          api_channel_categories
 22021  POST             /api/channel/set                                 api_channel_set
 21831  GET              /api/channels/status                             api_channels_status
 20707  POST             /api/chat/send                                   api_chat_send
 13386  GET              /api/chat/send_status                            api_chat_send_status
 10490  GET              /api/checks                                      api_checks
 21336  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 21319  GET              /api/clips                                       api_clips
 21352  POST/DELETE      /api/clips/clear                                 api_clips_clear
 20985  GET              /api/cohost                                      api_cohost
 20997  POST             /api/cohost/config                               api_cohost_config
 14686  GET              /api/community/stats                             api_community_stats
 22655  GET              /api/data/export                                 api_data_export
 20911  GET              /api/debug/threads                               api_debug_threads
 23482  GET              /api/defense/attacks                             api_defense_attacks
 23449  GET              /api/defense/crowdsec                            api_defense_crowdsec
 23467  GET              /api/defense/fail2ban                            api_defense_fail2ban
 23173  GET              /api/defense/overview                            api_defense_overview
 13728  POST             /api/discord/announce                            api_discord_announce
 13456  GET              /api/discord/clips_week                          api_discord_clips_week
 13672  GET              /api/discord/community                           api_discord_community
 13414  GET              /api/discord/invite                              api_discord_invite
 12988  GET              /api/discord/overview                            api_discord_overview
 13074  POST             /api/discord/webhook_test                        api_discord_webhook_test
 14199  GET              /api/events                                      api_events
 13503  GET              /api/events/stream                               api_events_stream
 14212  GET              /api/forecast/storage                            api_forecast_storage
 12001  GET              /api/freeai/status                               api_freeai_status
 12930  GET              /api/health                                      api_health
 14230  GET              /api/heatmap/lives/<username>                    api_heatmap_lives
 14226  GET              /api/heatmap/recordings                          api_heatmap_recordings
 21034  GET              /api/highlights                                  api_highlights
 21046  POST             /api/highlights/config                           api_highlights_config
 21872  GET              /api/kick/channel                                api_kick_channel
 21893  POST             /api/kick/channel                                api_kick_channel_set
 12687  GET              /api/kick/oauth/callback                         api_kick_oauth_callback
 12755  POST             /api/kick/oauth/disconnect                       api_kick_oauth_disconnect
 12733  POST             /api/kick/oauth/redirect                         api_kick_oauth_redirect
 12672  GET              /api/kick/oauth/start                            api_kick_oauth_start
 12712  GET              /api/kick/oauth/status                           api_kick_oauth_status
 21111  GET/POST         /api/kick/sendcheck                              api_kick_sendcheck
 21180  POST             /api/kickmod/config                              api_kickmod_config
 21225  POST             /api/kickmod/import_badwords                     api_kickmod_import_badwords
 21239  GET              /api/kickmod/learned                             api_kickmod_learned
 21266  POST             /api/kickmod/learned/clear                       api_kickmod_learned_clear
 21246  POST             /api/kickmod/learned/promote                     api_kickmod_learned_promote
 21577  POST             /api/kickmod/say                                 api_kickmod_say
 21553  POST             /api/kickmod/start                               api_kickmod_start
 21151  GET              /api/kickmod/status                              api_kickmod_status
 21564  POST             /api/kickmod/stop                                api_kickmod_stop
 10370  POST             /api/login                                       dashboard_login_submit
 14671  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard
 14640  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 13351  GET              /api/notify/status                               api_notify_status
 13362  POST             /api/notify/test                                 api_notify_test
 10594  GET              /api/outcomes                                    api_outcomes
 22492  POST             /api/overlay/config                              api_overlay_config
 22479  POST             /api/overlay/event                               api_overlay_event
 22384  GET              /api/overlay/state                               api_overlay_state
 10627  GET              /api/profile/<username>                          api_profile
 14396  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk
 14238  GET              /api/profile/snapshots/<username>                api_profile_snapshots
 14361  GET              /api/proxy/heatmap                               api_proxy_heatmap
 14338  GET              /api/proxy/trend                                 api_proxy_trend
 12456  GET              /api/public/stats                                api_public_stats
 10470  GET              /api/pulse                                       api_pulse
 13806  GET              /api/recording-attempts                          api_recording_attempts
 20642  POST             /api/restream/<int:rid>/delete                   api_restream_delete
 20620  POST             /api/restream/<int:rid>/edit                     api_restream_edit
 20661  POST             /api/restream/<int:rid>/start                    api_restream_start
 20932  POST             /api/restream/<int:rid>/stop                     api_restream_stop
 22346  GET              /api/restream/chatfeed                           api_restream_chatfeed
 20596  POST             /api/restream/create                             api_restream_create
 12763  GET              /api/restream/deck                               api_restream_deck
 11937  GET              /api/restream/health                             api_restream_health
 22368  POST             /api/restream/layout                             api_restream_layout
 20569  GET              /api/restream/list                               api_restream_list
 11906  POST             /api/restream/report                             api_restream_report
 20945  POST             /api/restream/start_all                          api_restream_start_all
 20971  POST             /api/restream/stop_all                           api_restream_stop_all
 12112  GET              /api/restream/testpush                           api_testpush_status
 12137  POST             /api/restream/testpush                           api_testpush_run
 14771  GET              /api/restream/verify                             api_restream_verify
 13434  GET              /api/retention/preview                           api_retention_preview
 13443  POST             /api/retention/run                               api_retention_run
 14155  GET              /api/search                                      api_search
 23220  GET              /api/selftest                                    api_selftest
 20678  GET              /api/shield/stats                                api_shield_stats
 10531  GET              /api/storage                                     api_storage
 10538  POST             /api/storage/cleanup                             api_storage_cleanup
 14292  GET              /api/stream/inspect/<username>                   api_stream_inspect
 11876  GET              /api/stream/timeline                             api_stream_timeline
 13062  GET              /api/stream/transcript                           api_stream_transcript
 10562  GET              /api/summary/preview                             api_summary_preview
 13871  GET              /api/system                                      api_system
 14719  GET              /api/system/check_timing                         api_check_timing
 15042  GET              /api/system/config_drift                         api_config_drift
 13098  GET              /api/system/config_snapshot                      api_system_config_snapshot
 13209  GET              /api/system/preflight                            api_system_preflight
 13335  GET              /api/system/preflight_history                    api_system_preflight_history
 13568  GET              /api/system/resilience                           api_system_resilience
 14190  GET              /api/tags                                        api_tags_list
 10504  GET              /api/top                                         api_top
 10863  GET              /api/trend-7d                                    api_trend_7d
 21384  GET              /api/tts/<fn>                                    api_tts_file
 15014  GET              /api/twitch/oauth/callback                       api_twitch_oauth_callback
 14966  POST             /api/twitch/oauth/redirect                       api_twitch_oauth_redirect
 14990  GET              /api/twitch/oauth/start                          api_twitch_oauth_start
 14944  GET              /api/twitch/oauth/status                         api_twitch_oauth_status
 22520  GET              /api/upload_window                               api_upload_window
 10608  GET              /api/userstats                                   api_userstats
 12504  GET              /api/version                                     api_version
 14865  GET              /api/youtube/oauth/callback                      api_youtube_oauth_callback
 14886  POST             /api/youtube/oauth/forget                        api_youtube_oauth_forget
 14898  POST             /api/youtube/oauth/logout                        api_youtube_oauth_logout
 14823  POST             /api/youtube/oauth/redirect                      api_youtube_oauth_redirect
 14847  GET              /api/youtube/oauth/start                         api_youtube_oauth_start
 14801  GET              /api/youtube/oauth/status                        api_youtube_oauth_status
 26910  GET              /api/youtube/sendrate                            api_youtube_sendrate
 13844  GET              /archive/<int:eid>/download                      archive_download
 13901  GET              /download/<int:recording_id>                     download
 13784  GET              /health                                          health
 20880  GET              /healthz                                         healthz
 10361  GET              /login                                           dashboard_login_page
 10391  GET              /logout                                          dashboard_logout
 10398  GET              /manifest.webmanifest                            pwa_manifest
 13126  GET              /metrics                                         api_prometheus_metrics
 22329  GET              /overlay                                         overlay_page
 10422  GET              /pwa-icon-<variant>.png                          pwa_icon
 10408  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (183)

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
   148  GET              /api/evolution/changelog                         api_evolution_changelog   [nc/routes/evolution.py]
   133  GET              /api/evolution/history                           api_evolution_history   [nc/routes/evolution.py]
    73  GET              /api/evolution/learned                           api_evolution_learned   [nc/routes/evolution.py]
    95  GET              /api/evolution/proposals                         api_evolution_proposals   [nc/routes/evolution.py]
   116  POST             /api/evolution/proposals/<int:pid>/dismiss       api_evolution_dismiss   [nc/routes/evolution.py]
    63  POST             /api/evolution/run                               api_evolution_run   [nc/routes/evolution.py]
   163  GET              /api/evolution/snapshots                         api_evolution_snapshots   [nc/routes/evolution.py]
    27  GET              /api/evolution/status                            api_evolution_status   [nc/routes/evolution.py]
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
    61  POST             /api/marketing/config                            api_marketing_config   [nc/routes/marketing.py]
    86  GET              /api/marketing/preview                           api_marketing_preview   [nc/routes/marketing.py]
    96  POST             /api/marketing/send-now                          api_marketing_send_now   [nc/routes/marketing.py]
    35  GET              /api/marketing/status                            api_marketing_status   [nc/routes/marketing.py]
    53  POST             /api/marketing/toggle                            api_marketing_toggle   [nc/routes/marketing.py]
   206  GET              /api/moderation/feed                             api_moderation_feed   [nc/routes/stats.py]
    83  POST             /api/news/config                                 api_news_config   [nc/routes/news.py]
    49  GET              /api/news/creators                               api_news_creators   [nc/routes/news.py]
    60  POST             /api/news/creators/generate                      api_news_creators_generate   [nc/routes/news.py]
   125  POST             /api/news/generate-now                           api_news_generate_now   [nc/routes/news.py]
   120  GET              /api/news/items                                  api_news_items   [nc/routes/news.py]
   111  GET              /api/news/preview                                api_news_preview   [nc/routes/news.py]
    36  GET              /api/news/status                                 api_news_status   [nc/routes/news.py]
    75  POST             /api/news/toggle                                 api_news_toggle   [nc/routes/news.py]
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
   109  GET              /api/streamer/compare                            api_streamer_compare   [nc/routes/streamer.py]
   256  POST             /api/streamer/delete/<username>                  api_streamer_delete   [nc/routes/streamer.py]
    71  GET              /api/streamer/detail                             api_streamer_detail   [nc/routes/streamer.py]
   281  GET              /api/streamer/digest/<username>                  api_streamer_digest   [nc/routes/streamer.py]
   213  GET              /api/streamer/dormant                            api_streamer_dormant   [nc/routes/streamer.py]
   237  GET              /api/streamer/exists/<username>                  api_streamer_exists   [nc/routes/streamer.py]
   168  GET              /api/streamer/journal/<username>                 api_streamer_journal   [nc/routes/streamer.py]
   133  GET/POST         /api/streamer/priority/<username>                api_streamer_priority   [nc/routes/streamer.py]
   193  GET              /api/streamer/watchlist                          api_streamer_watchlist   [nc/routes/streamer.py]
    39  GET              /api/streamers/wall                              api_streamers_wall   [nc/routes/streamer.py]
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
 23925  /ai                     AZRAEL / KI fragen (Text oder Sprachnachricht)
 24384  /ask                    AZRAEL etwas fragen — der KI-Community-Assistent
 24016  /assign_role            Rolle/Gruppe einem Mitglied geben
 24062  /ban                    Mitglied bannen
 24716  /botstats               Bot-Health: Uptime, Trackings, Aufnahmen, DB (Admin)
 24640  /clearwarns             Alle Verwarnungen eines Mitglieds löschen
 24680  /clip                   Highlight-Clip der letzten Sekunden vom laufenden Stream
 24665  /clipoftheweek          Aktuell führender Clip-of-the-Week (⭐-Voting)
 24507  /clips                  Letzte Highlight-Clips eines Users
 23977  /create_category        Kategorie anlegen
 23946  /create_channel         Text-Channel anlegen (optional in Kategorie)
 24005  /create_group           Nutzergruppe (= Rolle) anlegen
 23988  /create_role            Rolle / Nutzergruppe anlegen
 23962  /create_voice           Voice-Channel anlegen
 24298  /daily                  Tägliche XP-Belohnung abholen (Streak-Bonus!)
 24414  /event                  Community-Event ankündigen (Admin) — mit Countdown
 24457  /events                 Kommende Community-Events anzeigen
 24553  /follow                 Bei Live-Gang eines Streamers gepingt werden
 24537  /help                   Alle Bot-Befehle anzeigen
 24051  /kick                   Mitglied kicken
 24280  /leaderboard            Top-10 der Community nach XP
 24493  /livenow                Welche getrackten User sind gerade live
 24523  /post_test              Test: Nachricht in den Channel eines getrackten Users posten
 24354  /profile                Dein Community-Profil: Level, Rang, Streak, Rang-Platz
 24086  /purge                  Letzte N Nachrichten im Channel löschen (max 100)
 24266  /rank                   Dein Level und Rang anzeigen
 24480  /recstatus              Aktuell laufende Aufnahmen
 24027  /remove_role            Rolle/Gruppe entfernen
 23939  /restream_status        Restream-Status
 24038  /set_channel_perms      Rechte einer Rolle für einen Channel setzen
 24231  /setup_community        Community-Server einrichten: Ränge, Channels, Rechte
 24249  /setup_targets          Pro getracktem User: Clips-, Chat- und Voice-Channel anlegen
 24579  /stats                  Statistik zu einem getrackten Streamer
 23851  /status                 Azrael Sentinel Status: Trackings, Live, Restream
 24875  /streaminfo             Kompakt-Karte eines Streamers: Aktivität, Aufnahmen, Followe
 24772  /sys_report             Azrael Sentinel Wochenreport (Brain, Markdown)
 24748  /sys_unpause            Auto-pausierte Quelle wieder aktivieren (Admin)
 24073  /timeout                Mitglied stummschalten (Minuten)
 24651  /topstreamers           Rangliste der Streamer nach Aufnahmen
 23881  /track                  TikTok-User tracken
 23865  /tracklist              Getrackte TikTok-User dieses Servers
 24568  /unfollow               Live-Pings für einen Streamer abbestellen
 23914  /untrack                TikTok-User nicht mehr tracken
 24601  /warn                   Mitglied verwarnen (eskaliert ab 3 Verwarnungen zu Timeout)
 24625  /warnings               Verwarnungen eines Mitglieds anzeigen
```

## Discord-Events (4)

```
 25359  on_member_join
 25321  on_message
 24962  on_raw_reaction_add
 25394  on_ready
```

## Top-Level-Symbole in bot.py (519 Funktionen, 2 Klassen)

```
  2481-2482   _abo_key
  2502-2520   _abo_probe_dump
 22762-22772  _active_recorder_sync
 17863-17870  _ad_allowlist
 18985-18991  _agent_for
 22774-22792  _ai_calls_total_sync
 18994-19010  _ai_telemetry
 19492-19510  _alert
 25510-25560  _alert_monitor_loop
 25941-26003  _announce_loop
  3423-3426   _anthropic_key
  3433-3435   _anthropic_model
 10114-10117  _arg_int
  2473-2478   _as_dict
 15723-15728  _audio_cfg
 19646-19668  _audio_tap_cmd
 10282-10293  _auth_cookie
 10249-10278  _auth_guard
  1629-1634   _auto_on
 20545-20563  _auto_restream_loop
 27071-27086  _azrael_broadcast_reply
 26971-26993  _azrael_chat_reply
 26954-26968  _azrael_chat_should_reply
 26999-27001  _azrael_gate_cfg
 19015-19029  _azrael_live_state
 22232-22246  _azrael_overlay_state
 19375-19429  _azrael_proactive_loop
 18834-18890  _azrael_reaction_to_chats
 27004-27011  _azrael_reply_all_chats
 26941-26951  _azrael_self_names
 27039-27068  _azrael_send_to
 19032-19053  _azrael_system
 25679-25682  _backup_active
 25760-25773  _backup_loop
 17751-17752  _badwords_path
 25472-25481  _brain_growth_loop
 10939-10966  _brain_growth_snapshot
  2409-2429   _brain_hint_delay
 10931-10933  _brain_history_for
  6502-6530   _brain_notify
 10908-10929  _brain_record
 10935-10937  _brain_stream_recent
 13482-13499  _browser_push
  6546-6633   _build_daily_summary
  2912-3092   _build_native_cmd
 16071-16258  _build_restream_cmd
  3136-3169   _build_ytdlp_cmd
 22714-22721  _cached_probe
  5324-5351   _can_stop_tracking
  1809-1831   _capture_set_cookies
 14455-14458  _cfg_get
 14461-14463  _cfg_set
 21976-22011  _channel_set_all
 15321-15324  _chat_connected
 15327-15343  _chat_disconnected
  8594-8605   _chat_is_forum
 15363-15365  _chat_sanitize
 15367-15376  _chat_src_ok
 15306-15318  _chat_stat
 15346-15349  _chat_stats_snapshot
  3698-3709   _check_ai_alive_sync
  3712-3724   _check_ai_models_sync
 22723-22736  _check_redis_alive_sync
 22738-22758  _check_redis_version_sync
 11538-11581  _classify_pool_anonymity
 11584-11601  _classify_pool_anonymity_bg
   787-791    _claude_chat_sync_metered
 10143-10150  _client_ip
 26035-26062  _clip_prune
 26065-26075  _clip_recfile_for
 26591-26597  _clip_should_velocity
 26116-26198  _clip_to_discord
  3596-3605   _close_ai_session
 27115-27130  _cohost_broadcast
 27097-27101  _cohost_cfg
 27156-27168  _cohost_fire_highlight
 27104-27112  _cohost_gate
 27133-27153  _cohost_highlight
 26247-26281  _community_events_loop
 10762-10764  _conv_messages
  6935-6978   _cookie_alarm_loop
  1881-1885   _cookie_autorefresh_info
  1786-1790   _cookie_header
 13532-13564  _cpu_load_snapshot
  3906-3918   _create_index_safe
 22975-23081  _crowdsec_status
 22941-22972  _crowdsec_via_lapi
 22806-22824  _cscli_bin
 22830-22843  _cscli_path
  6825-6850   _daily_summary_loop
 22861-22878  _darf_journal_lesen
 25484-25507  _db_maintenance_loop
  6794-6822   _db_vacuum_loop
 17886-17910  _detect_foreign_ad
  1367-1378   _diag_path_owner
 19281-19325  _director_finalize
 20092-20099  _director_for
 19230-19278  _director_mark
 26485-26520  _disc_automod_check
 26458-26464  _disc_state_get
 26467-26474  _disc_state_set
 23524-23537  _discord_guild_filesize_bytes
 23723-23732  _discord_invite
 26419-26455  _discord_live_thread
 19432-19444  _discord_notify
 23624-23649  _discord_ops_alert
 26317-26415  _discord_post_user
 23788-25469  _discord_run_once
 23662-23720  _discord_start
 26006-26012  _discord_stop
 23545-23547  _discord_upload_limit_label
 23540-23542  _discord_upload_limit_mb
  6853-6930   _disk_alarm_loop
 28517-28566  _disk_autoclean
 28569-28582  _disk_guard_loop
 28509-28514  _disk_pct
 15680-15682  _drawtext_chain
 13998-14000  _dump_all_threads
 11463-11527  _enrich_proxies_with_geo
  2026-2070   _ensure_cookie_file_netscape
 23735-23785  _ensure_discord_invite
 26212-26244  _ensure_error_channel
  8653-8656   _ensure_notify_topic
 11708-11745  _ensure_proxy_ready
  8607-8634   _ensure_topic
   650-652    _env_int
   655-657    _env_int_range
 26284-26314  _error_channel_loop
 19476-19489  _event_webhook
 15129-15142  _evolution_loop
  5944-5978   _extract_file_payload
  2158-2160   _extract_urls_from_streamurl_node
 22846-22853  _f2b_sudo_hint
 19512-19514  _faster_whisper_available
 17775-17787  _fetch_ldnoobw_de
 11352-11370  _fetch_proxy_list
 19926-19954  _fetch_tiktok_room_id
   721-724    _ff_cmd
 15843-15848  _find_chromium
  3129-3133   _find_external_recorder
  2163-2165   _find_stream_urls
 14506-14531  _fire_webhooks
  7714-7723   _fork_safe
   802-811    _freeai_chat_sync_metered
 22896-22938  _geo_lookup_ips
  3585-3594   _get_ai_session
  7548-7588   _get_live_info
  2699-2706   _get_resolve_semaphore
  7949-8315   _handle_single_tracking
 28361-28363  _hb
 28366-28383  _hb_while
 15381-15383  _highlight_cfg
 15386-15415  _highlight_observe
 15851-15856  _htmlov_screenshot_cmd
 19670-19680  _httpx_proxy
 14539-14551  _in_quiet_hours
 29396-29427  _install_fast_eventloop
 10009-10063  _install_fast_json
 14003-14019  _install_faulthandler
 20788-20797  _intel_ensure_schema
 20835-20870  _intel_index_loop
 20809-20819  _intel_index_one
 20800-20806  _intel_semantic
  5313-5322   _is_authorized
  7879-7885   _is_dead
  2148-2150   _is_hevc
 22881-22887  _is_private_ip
  1531-1538   _is_process_running
  6532-6543   _is_quiet_hours
  1168-1177   _is_upload_window
 10098-10111  _json_error_handler
  6752-6782   _kick_broadcaster_id
 12038-12057  _kick_channel_live
  6666-6708   _kick_follower_count
 12650-12663  _kick_oauth_exchange
 12666-12668  _kick_oauth_page
 12609-12613  _kick_redirect_public
 12604-12606  _kick_redirect_source
 12596-12601  _kick_redirect_uri
  6651-6653   _kick_slug
 12616-12647  _kick_user_token
  3955-3958   _kind_from_filename
 14568-14573  _latest_popularity
 17797-17803  _learned_load
 17794-17795  _learned_path
 17805-17813  _learned_save
 20307-20340  _live_react_loop
 20103-20296  _live_react_worker
 18893-18904  _live_transcript_push
 20298-20305  _live_users
 19328-19372  _living_title_loop
 17754-17762  _load_banned_words_file
  1707-1780   _load_cookies_dict
 25685-25757  _local_backup_scan
 10080-10094  _log_5xx
 16266-16278  _looks_like_codec_err
 16261-16263  _looks_like_source_expired
  7795-7825   _loop_fehler
 14023-14032  _loop_heartbeat
 28331-28358  _loop_lag_monitor
 14035-14103  _loop_watchdog_thread
 18773-18787  _loyalty_add
 18764-18770  _loyalty_get
 18790-18798  _loyalty_top
 14705-14707  _manual_donations_total
  7887-7888   _mark_dead
 12209-12225  _marketing_loop
 27018-27036  _maybe_handle_command
 28668-28692  _maybe_hype_clip
  3873-3896   _migrate_columns
 27295-27306  _mod_is_exempt
 27309-27314  _mod_warn_first
 27317-27320  _mod_warn_text
 15169-15177  _modlog
   921-923    _multistream_targets
  7726-7727   _nc_create_subprocess_exec
  7730-7731   _nc_create_subprocess_shell
 12461-12478  _news_loop
 15207-15209  _normalize_ingest
  2340-2357   _note_check_duration
  8647-8650   _notify_topic_name
 12560-12571  _oauth_redirect_env
 12587-12593  _oauth_redirect_source
 12574-12584  _oauth_redirect_uri
 18919-18927  _oracle_memories
 19185-19219  _oracle_memorize
 18930-18943  _oracle_persona
 18912-18916  _oracle_recent_text
 15506-15514  _ov_atomic_write
 15494-15500  _ov_bar
 17710-17722  _ov_clip_text
 15503-15504  _ov_oneline
 22296-22325  _overlay_push
 15797-15840  _overlay_render_size
 15268-15272  _overlay_session_reset
 22248-22251  _overlay_src_ok
 17873-17883  _own_invites
 15792-15794  _parse_size
 23089-23169  _parse_ssh_attacks
  7150-7183   _pause_resume_cmd
  1835-1879   _persist_refreshed_cookies
  1673-1705   _pick_checked_pull_proxy
 10179-10192  _pin_auth_value
 10238-10239  _pin_clear_fail
 10218-10221  _pin_locked
 10224-10235  _pin_note_fail
 10195-10215  _pin_ok
 22138-22140  _piper_available
 22103-22125  _piper_list_voices
 22145-22170  _piper_pick_model
 22182-22229  _piper_say
 22096-22100  _piper_voice_roots
 14468-14503  _post_json_threaded
 15771-15789  _probe_video_size
  1559-1576   _proc_is_recorder
 11450-11461  _proxy_geo_cache_put
 11677-11705  _proxy_pool_refresh_loop
  1639-1670   _proxy_report_recording
 13988-13990  _prune_stall_dumps
 12519-12557  _public_base_url
 12279-12400  _public_stats
 19447-19473  _push_notify
 10340-10342  _pwa_dir
 11421-11436  _quick_validate_proxy
 14534-14536  _quiet_hours_config
 10305-10338  _rate_guard
 18738-18744  _react_warn
  7634-7673   _reap_proc
  2380-2402   _record_check_outcome
   716-718    _redact_stream_urls
 11604-11674  _refresh_proxy_pool
 22128-22134  _resolve_piper_model
  2174-2264   _resolve_via_html
  2522-2676   _resolve_via_webcast_api_v2
  2739-2801   _resolve_via_ytdlp
 26637-26766  _resolve_youtube_ingest
 20379-20386  _restream_active_platforms
 15253-15264  _restream_active_sources
 19957-20056  _restream_chat_guardian
 15418-15490  _restream_chat_push
 15180-15192  _restream_enabled
 15859-15946  _restream_html_overlay_start
 15949-15962  _restream_html_overlay_stop
  1116-1118   _restream_layout_mode
 15218-15241  _restream_overlay_files
 20344-20376  _restream_platform_state
 20507-20542  _restream_resume_after_restart
 16010-16068  _restream_tts_enqueue_wav
 15733-15765  _restream_tts_feeder
 15730-15731  _restream_tts_fifo_path
 15965-15992  _restream_tts_start
 15994-16008  _restream_tts_stop
 20389-20504  _restream_verify_loop
 25650-25662  _retention_loop
 25609-25647  _retention_scan
  2484-2486   _room_is_abo
  5982-6099   _run_ai_call
 14126-14139  _run_async_from_flask
 22890-22893  _run_priv
 29384-29392  _run_selfcheck_and_exit
 25665-25676  _s3_client
  7890-7936   _safe_send
  4577-4593   _sample_net_throughput
 17764-17772  _save_banned_words_file
  2432-2459   _schedule_next_check
 25563-25606  _scheduler_loop
  3899-3903   _schema_pk
 14143-14148  _scraper_session
 27323-27362  _screen_full
 12946-12983  _sec_headers
  2153-2155   _select_stream_from_data_section
 29197-29381  _selfcheck
  8659-8693   _send_live_notice
  1191-1195   _should_defer_upload
 26078-26113  _shrink_for_discord
 10345-10357  _sicheres_ziel
 28589-28606  _sign_health_check
 28609-28628  _sign_health_loop
  7743-7754   _spawn
  7757-7787   _spawn_from_flask
 23213-23216  _st_befund
 19682-19923  _start_chat_listener
 14106-14123  _start_loop_watchdog
 12424-12452  _stats_loop
 12403-12406  _stats_output_path
 12409-12421  _stats_write
  8387-8403   _storage_cleanup_loop
 28648-28655  _story_for
  3191-3197   _stream_url_expiry
  3206-3212   _stream_url_is_fresh
  3199-3204   _stream_url_ttl
 17837-17844  _streamer_persona_get
 17819-17825  _streamer_personas_load
 17816-17817  _streamer_personas_path
 17827-17835  _streamer_personas_save
 15685-15689  _studio_chain
 25782-25904  _system_backup
 25907-25937  _system_backup_loop
 11373-11412  _test_proxy
 12079-12088  _testpush_cfg
 12091-12108  _testpush_exec
 12060-12076  _testpush_resolve_live
  8566-8576   _tg_topics_load_into_mem
  8563-8564   _tg_topics_path
  8578-8585   _tg_topics_save
 10153-10161  _token_ok
  8588-8592   _topic_forget
 14554-14565  _tracking_max_duration
  4164-4178   _tracking_remove_cleanup
  4195-4207   _tracking_resume_cleanup
  1425-1448   _try_attach_file_handler
 22172-22180  _tts_cleanup
 12016-12020  _tunnel_effective
 21598-21651  _twitch_channel_status
 27365-27508  _twitch_chat_loop
 27179-27282  _twitch_eventsub_loop
 15035-15038  _twitch_oauth_page
  1214-1227   _upload_queue_add
  1238-1240   _upload_queue_count
  1197-1206   _upload_queue_load
  1187-1189   _upload_queue_path
  1229-1236   _upload_queue_remove
  1208-1212   _upload_queue_save
  1242-1283   _upload_window_loop
  7607-7614   _uptime_s
 15195-15204  _url_host
   696-713    _url_ohne_zugang
   780-784    _usage_record_claude
  7828-7872   _verbindung_verloren
  6711-6742   _viewer_sample_loop
  6784-6791   _viewer_stats
 10242-10245  _wants_html
  7617-7631   _warn_empty_env
 28404-28499  _watchdog_loop
 26920-26928  _wchat_thank_ok
 19516-19546  _whisper_get_model
  7704-7711   _whisper_native_section
 18725-18731  _whisper_pool
 19615-19644  _whisper_segments
 19548-19612  _whisper_transcribe
 15516-15678  _write_restream_overlay
 27536-27615  _youtube_api_chat_loop
 21654-21757  _youtube_api_status
 21760-21827  _youtube_channel_status
 27618-27778  _youtube_chat_loop
 26772-26785  _youtube_restream_autoconfig
 26788-26812  _youtube_restream_autoconfig_inner
 26878-26906  _youtube_send
 21932-21973  _youtube_set_channel
 26815-26849  _yt_access_token
 26852-26867  _yt_live_chat_id
 27529-27533  _yt_oauth_configured
 26873-26875  _yt_sendrate_cfg
 27511-27526  _yt_timeout
  2723-2724   _ytdlp_detect_available
  2726-2737   _ytdlp_note_result
 13993-13995  _zombie_child_count
  7484-7508   about
  4074-4078   add_ai_log_entry
  3991-3994   add_archive_entry
  4690-4705   add_archive_rule
  4366-4400   add_recording
  4139-4156   add_tracking
  6102-6135   ai
  3738-3777   ai_chat
  3811-3821   ai_history_append
  3823-3828   ai_history_clear
  3800-3809   ai_history_load
  3785-3798   ai_rate_limit_check
  6164-6172   aireset
 19056-19075  azrael_chat
 27783-27905  brain_cmd
  3215-3399   build_recording_cmd
  4159-4162   bulk_add_trackings
  6981-7040   bulkadd
  8406-8546   check_all_trackings
  4211-4223   claim_live_transition
 17913-18668  class KickModerator
 16281-17597  class RestreamManager
 11790-11832  classify_proxy_anonymity
  6210-6408   cleanup
  5173-5214   cleanup_old_recordings
  4357-4364   clear_recording
 26523-26588  clip_moment
  4521-4570   compute_storage_forecast
  7103-7147   cookies_cmd
  4130-4136   count_trackings_for_chat
  4061-4072   decide_preferred_recorder
  4001-4004   delete_archive_entry
  4707-4715   delete_archive_rule
  5639-5786   diag
 28017-28078  einnahmen_cmd
  4515-4518   find_recordings_by_fingerprint
  4022-4038   finish_recording_attempt
  4183-4185   get_all_active_trackings
  4089-4092   get_all_checks
  4402-4405   get_all_recordings
  4464-4466   get_all_tags_with_counts
  4492-4495   get_annotations_for_recording
  3996-3999   get_archive_entry
  4485-4488   get_bookmarked_recordings
  1902-2019   get_cookie_health
  4452-4458   get_event_log
  4045-4059   get_last_recording_attempt
  2804-2909   get_live_status
  4973-4976   get_manual_recordings
  4500-4503   get_or_compute_inspect_sync
  5249-5293   get_outcome_breakdown
  4471-4474   get_priority_poll_interval
  4668-4677   get_profile_snapshots
  4040-4043   get_recent_recording_attempts
  4407-4410   get_recording_by_id
  4478-4481   get_recording_note
  3533-3556   get_redis
  4119-4122   get_stats
  5140-5171   get_storage_stats
  4808-4810   get_tiktok_status_distribution
  4225-4234   get_tracking_state
  4180-4181   get_trackings_for_group
  4989-4992   get_trash_recordings
  9314-9977   handle_recording_finished
  3921-3946   init_db
  5063-5117   inspect_stream_url
 22291-22293  is_revenue_platform
  4680-4688   list_archive_rules
  5443-5481   live
  7939-7947   live_check_worker
  3608-3642   llm_chat
  3665-3693   llm_chat_sync
  3650-3662   llm_list_models
  4418-4444   log_event
  1493-1526   log_recording_failure
  7297-7346   logs_cmd
 28696-29187  main
  6138-6161   on_ai_media
  7423-7449   on_ai_reply
  7452-7481   on_azrael_mention
  7513-7543   on_callback
 19078-19182  oracle_handle
  7186-7189   pause_tracking
  5303-5308   profile_keyboard
  7248-7294   quota
  8317-8384   reaper_loop
  4804-4806   record_tiktok_status
  6177-6207   recstatus
  3558-3566   redis_get_json
  3568-3574   redis_set_json
 28081-28091  report_cmd
 11835-11837  report_proxy_result
  2267-2294   resolve_tiktok_live_stream
  4984-4987   restore_recording
  7192-7195   resume_tracking
  4718-4798   run_archive_rules
 28094-28311  run_bot
 13915-13962  run_flask
  4596-4641   sample_bandwidth_for_active
  4647-4666   save_profile_snapshot
  4081-4087   save_tiktok_check
  4349-4355   set_recording_file
  4188-4192   set_tracking_paused
  4979-4982   soft_delete_recording
  8699-9312   split_and_send_video
  5356-5398   start
  4006-4020   start_recording_attempt
  6411-6449   stats
  4954-4971   stop_manual_recording
  7198-7245   stoprec
  6636-6644   summary_cmd
  7349-7420   sysres
  5788-5932   teststream
  5400-5441   tiktok
  7043-7100   topusers
  5518-5575   track
  5483-5515   track_exact
  5589-5637   tracklist
  4820-4952   trigger_manual_recording
  4310-4347   try_acquire_recording_lock
  4995-5054   universal_search
  5577-5587   untrack
 27908-28014  update_cmd
  4510-4513   update_recording_fingerprint
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
evolution.py           analyze, build_dir, conf, configure, cycle, engineering_note, next_version, write_build
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
marketing.py           ai_flavor, class MarketingConfig, class MarketingState, compose, config, configure, default_targets, enabled, has_content, next_due_ts, post_discord, post_telegram, publish, should_post, state, state_save, variants
modheuristics.py       caps_ratio, count_links, count_mentions, escalation_minutes, escalation_step, flood_reason, is_caps_spam, is_exempt, kick_roles, prune_history, prune_infractions, resolve_exempt, stateless_reason, twitch_roles
netstat.py             sum_bytes, throughput_kbps
news.py                absaetze, azrael_creator_take, build_items, class NewsConfig, class NewsState, collect_facts, config, configure, creator_activity, creator_dossier_generate, creator_facts_line, enabled, generate, item_id, merge, output_path, phrase, phrase_impl, read_items, render_json, should_generate, state, state_save, write_items
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
tiktokcheck.py         account_exists, configure
trackingdb.py          add_tracking_tag, bulk_add_trackings, ci_key, claim_transition, configure, get_all_active_trackings, get_all_tags_with_counts, get_priority_poll_interval, get_state, get_tags_for_tracking, get_tracking_priority, get_trackings_for_group, remove_tracking, remove_tracking_tag, resolve_tracked_user, set_tracking_paused, set_tracking_priority
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
